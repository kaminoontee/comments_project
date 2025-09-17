from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    homepage = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # для вложенных комментариев
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    file = models.FileField(upload_to="uploads/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


class Captcha(models.Model):
    question = models.CharField(max_length=20)
    answer = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate():
        import random
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        question = f"{a} + {b} = ?"
        answer = str(a + b)

        # Перед созданием новой капчи — чистим старые
        Captcha.cleanup()

        return Captcha.objects.create(question=question, answer=answer)

    @staticmethod
    def cleanup():
        """Удаляем капчи старше 5 минут"""
        expiry_time = timezone.now() - timedelta(minutes=5)
        Captcha.objects.filter(created_at__lt=expiry_time).delete()