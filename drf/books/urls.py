from django.urls import path

from .views import (
    home,
    UserAPIView,
)

urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>/', UserAPIView.as_view()),
]
