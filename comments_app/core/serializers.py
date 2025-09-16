import re
from rest_framework import serializers
from .models import User, Comment
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Captcha

from rest_framework import serializers

from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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

        # Ограничение по размеру (100KB)
        if file.size > 100 * 1024:
            raise serializers.ValidationError("File size must be <= 100KB.")

        # Проверка формата
        if file.content_type in ["image/jpeg", "image/png", "image/gif"]:
            # Проверяем размеры
            image = Image.open(file)
            w, h = image.size
            if w > 320 or h > 240:
                # Пропорциональное уменьшение
                image.thumbnail((320, 240))

                # Сохраняем в память
                output = io.BytesIO()
                image.save(output, format=image.format)
                output.seek(0)

                # Перезаписываем file как новый InMemoryUploadedFile
                file = InMemoryUploadedFile(
                    output,
                    "file",
                    file.name,
                    file.content_type,
                    sys.getsizeof(output),
                    None,
                )
        elif file.content_type == "text/plain":
            pass  # ок
        else:
            raise serializers.ValidationError("Only JPG, PNG, GIF images or text files are allowed.")

        return file

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and hasattr(obj.file, "url"):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

class CaptchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captcha
        fields = ["id", "question"]
