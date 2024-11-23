# from django.urls import path, re_path
from django.urls import re_path

from .views import (
    BookAPIView,
    books_view,
    BookDjangoFiltersAPIView,
    book_list,
)

urlpatterns = [
    re_path(r'^books/$', BookDjangoFiltersAPIView.as_view()),
    # re_path(r'^books/(?P<category>.+)/$', BookDjangoFiltersAPIView.as_view()),
    # path("books/", BookDjangoFiltersAPIView.as_view()),
    # path("books/", book_list),
]
