from django.urls import path

from .views import (
    BookAPIView,
    ProtectedView,
)

urlpatterns = [
    # path('<int:pk>/', BookAPIView.as_view()),
    # path('', BookAPIView.as_view()),
    path('', ProtectedView.as_view()),
]
