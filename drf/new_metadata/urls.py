

from django.urls import path

from .views import (
    ManagerListAPIView,
)


urlpatterns = [
    path('', ManagerListAPIView.as_view()),
]
