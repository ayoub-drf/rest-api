from django.urls import path
from .views import (
    PostAPIView
)

urlpatterns = [
    path('posts/', PostAPIView.as_view(), name="Posts"),
    path('posts/<int:pk>/', PostAPIView.as_view(), name="Post_detail"),
]
