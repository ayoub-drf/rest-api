from .views import Books

from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path, re_path

urlpatterns = [
    path('books', Books.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
