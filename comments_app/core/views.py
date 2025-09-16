from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Comment, User, Captcha
from .serializers import CommentSerializer

from .serializers import CaptchaSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().select_related("user").prefetch_related("replies").order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["user__username", "user__email", "created_at"]  # разрешённые поля сортировки
    ordering = ["-created_at"]  # сортировка по умолчанию: новые сверху (LIFO)

    def perform_create(self, serializer):
        user_data = self.request.data.get("user", {})
        user, _ = User.objects.get_or_create(
            email=user_data.get("email"),
            defaults={
                "username": user_data.get("username"),
                "homepage": user_data.get("homepage"),
            }
        )
        serializer.save(user=user)


class CaptchaView(APIView):
    def get(self, request):
        captcha = Captcha.generate()
        return Response(CaptchaSerializer(captcha).data)

class CommentRetrieveView(generics.RetrieveAPIView):
    queryset = Comment.objects.all().select_related("user").prefetch_related("replies")
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]