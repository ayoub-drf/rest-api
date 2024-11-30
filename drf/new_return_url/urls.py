from django.urls import path

from .views import SimpleAPIView, SingleAPIView

urlpatterns = [
    path('', SimpleAPIView.as_view()),
    path('single/<int:year>', SingleAPIView.as_view(), name='single'),
]
