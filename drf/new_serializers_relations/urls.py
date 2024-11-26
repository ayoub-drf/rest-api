from django.urls import path

from .views import (
    index_1,
    BookRetrieveAPIView,
    index_1_single,
)

urlpatterns = [
    path("", index_1, name="libraries"),
    path("<int:pk>/", index_1_single, name="libraries-detail"),
    path("book/<int:pk>/", BookRetrieveAPIView.as_view(), name="book-detail"),
]
