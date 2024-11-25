from django.urls import path

from .views import (
    ProductListAPIView,
    ProductListAPIViewTwo
)

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('v2/', ProductListAPIViewTwo.as_view()),

]
