from .views import *

from django.urls import path

urlpatterns = [
    path('', SimpleAPIView.as_view())
]
