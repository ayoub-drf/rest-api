from .views import Books, book_view

from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path, re_path

urlpatterns = [
    # path('books', Books.as_view())
    path('books', book_view)
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', "yaml", "xml"])
