from django.urls import path

from .views import (
    index_1,
    BookCreateAPIView,
    EventCreateAPIView,
)

urlpatterns = [
    path('event/', EventCreateAPIView.as_view()),
    path('book/', BookCreateAPIView.as_view()),
    path('', index_1),
]
