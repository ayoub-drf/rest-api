from django.urls import path

from .views import (
    index_v1,
    index_v2,
    PersonsListAPIView,
)

urlpatterns = [
    path('', PersonsListAPIView.as_view()),
]
