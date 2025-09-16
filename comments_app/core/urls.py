from django.urls import path
from .views import CommentListCreateView, CaptchaView

urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comments"),
    path("captcha/", CaptchaView.as_view(), name="captcha"),
]
