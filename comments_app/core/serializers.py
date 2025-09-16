from rest_framework import serializers
from .models import User, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "homepage"]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at", "parent", "file", "replies"]

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data
