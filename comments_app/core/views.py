from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Comment, User
from .serializers import CommentSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().select_related("user").prefetch_related("replies")
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

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
