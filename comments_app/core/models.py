from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    homepage = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
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
