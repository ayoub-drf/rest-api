from django.urls import path

from .views import (
    MyView,
    api
)

urlpatterns = [
    path("", api)
]
