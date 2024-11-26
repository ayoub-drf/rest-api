from django.urls import path
from .views import (
    home_1,
    custom_serializer_one_view,
)

urlpatterns = [
    path('', custom_serializer_one_view),
]
