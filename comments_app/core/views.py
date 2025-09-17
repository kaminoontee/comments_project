import json

from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, User, Captcha
from .serializers import CommentSerializer, CaptchaSerializer

from .serializers import sanitize_text

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

class PreviewView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"html": sanitize_text(request.data.get("text", ""))})
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent__isnull=True).select_related("user").prefetch_related("replies")
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["user__username", "user__email", "created_at"]  # разрешённые поля сортировки
    ordering = ["-created_at"]  # сортировка по умолчанию: новые сверху (LIFO)

    def get_serializer_context(self):
        # пробросим request в сериализатор (чтобы file был полный URL и в replies)
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        # проверка капчи
        captcha_id = self.request.data.get("captcha_id")
        captcha_answer = self.request.data.get("captcha_answer")

        if not captcha_id or not captcha_answer:
            raise ValidationError({"captcha": "Captcha is required"})

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_id)
        except CaptchaStore.DoesNotExist:
            raise ValidationError({"captcha": "Invalid captcha"})

        if captcha.response != captcha_answer.lower():
            raise ValidationError({"captcha": "Incorrect captcha"})
        captcha.delete()  # удалить, чтобы нельзя было переиспользовать

        # создание пользователя
        username = self.request.data.get("username")
        email = self.request.data.get("email")
        homepage = self.request.data.get("homepage")

        if not username or not email:
            raise ValidationError({"user": "username and email are required"})

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": username, "homepage": homepage}
        )

        # поддержка ответов
        parent_id = self.request.data.get("parent")
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        serializer.save(user=user, parent=parent)


class CaptchaView(APIView):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        image_url = request.build_absolute_uri(captcha_image_url(new_captcha))
        return Response({"id": new_captcha, "image_url": image_url})

class CommentRetrieveView(generics.RetrieveAPIView):
    queryset = Comment.objects.all().select_related("user").prefetch_related("replies")
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

