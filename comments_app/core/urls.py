from django.urls import path
from .views import CommentListCreateView, CaptchaView, CommentRetrieveView, PreviewView

urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comments"),
    path("comments/<int:pk>/", CommentRetrieveView.as_view(), name="comment-detail"),
    path("captcha/", CaptchaView.as_view(), name="captcha"),
    path("preview/", PreviewView.as_view(), name="preview"),
]
