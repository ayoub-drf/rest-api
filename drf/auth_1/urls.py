from django.urls import path
from .views import (
    auth_1,
    register_1,
    SampleView
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/', SampleView.as_view()),
    path('', auth_1),
]
