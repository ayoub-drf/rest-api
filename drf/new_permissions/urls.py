from django.urls import path

from .views import (
    PersonRetrieveAPIView
)

urlpatterns = [
    path("persons/<int:pk>/", PersonRetrieveAPIView.as_view())
]
