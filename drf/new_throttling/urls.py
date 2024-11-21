from django.urls import path

from .views import (
    Register,
    register
)

urlpatterns = [
    # path('register/', Register.as_view())
    path('register/', register)
]
