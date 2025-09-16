import re
from rest_framework import serializers
from .models import User, Comment
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Captcha

# Допустимые HTML-теги
ALLOWED_TAGS = ["a", "code", "i", "strong"]

def sanitize_text(value):
    """Пропускаем только разрешённые HTML-теги"""
    import bleach
    return bleach.clean(value, tags=ALLOWED_TAGS, strip=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "homepage"]

    def validate_username(self, value):
        if not re.match(r"^[A-Za-z0-9]+$", value):
            raise serializers.ValidationError("Username must contain only Latin letters and digits.")
        return value

    def validate_homepage(self, value):
        if value:
            validator = URLValidator()
            try:
                validator(value)
            except ValidationError:
                raise serializers.ValidationError("Homepage must be a valid URL.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at", "parent", "file", "replies"]

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

    def validate_text(self, value):
        return sanitize_text(value)

    def validate_file(self, file):
        if not file:
            return file

        # Ограничение по размеру
        if file.size > 100 * 1024:
            raise serializers.ValidationError("File size must be <= 100KB.")

        # Проверка формата
        if file.content_type.startswith("image/"):
            w, h = get_image_dimensions(file)
            if w > 320 or h > 240:
                raise serializers.ValidationError("Image must be <= 320x240px.")
        elif file.content_type == "text/plain":
            pass  # ок
        else:
            raise serializers.ValidationError("Only images and text files are allowed.")

        return file

class CaptchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captcha
        fields = ["id", "question"]
