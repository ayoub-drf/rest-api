from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import (
    SearchFilter, 
    OrderingFilter,
)
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer

from .filters import (
    CustomTitleBaseFilterBackend,
    BookFilter,
)


# class BookDjangoFiltersAPIView(ListAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()

#     def get_queryset(self):
#         return Book.objects.all()

#     def filter_queryset(self, queryset):
#         category = self.kwargs.get('category')
#         return Book.objects.filter(categories__name=category)


class BookDjangoFiltersAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    # filterset_class = BookFilter or filterset_fields for fields without using an external class
    filterset_fields = ('id', 'stock', 'categories__name') # default lookup icontains
    # filterset_fields = ('$categories__name') # (^ istartswith) | (= iexact) | ($ iregex)


    # search_fields = ('id', 'categories__name') # SearchFilter to see a search input in BrowsableAPI

@api_view(['GET'])
def book_list(request):
    filter = BookFilter(request.GET, queryset=Book.objects.all())    
    products = filter.qs
    serializer = BookSerializer(products, many=True)

    return Response(serializer.data, 200)


class BookAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filter_backends = [CustomTitleBaseFilterBackend]

    # [ ?search=2022 or ?search=book ] by title or published_at
    # filter_backends = [SearchFilter,]
    # search_fields = ['title', 'published_at']

    # # [ ?ordering=-published_at ?ordering=id ] Filter by id or -published_at
    # filter_backends = [OrderingFilter,]
    # ordering_fields = ['title', 'published_at'] 
    # ordering = '-published_at' # Default order (books/)

    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.query_params.get('title', None)
        published_at = self.request.query_params.get('published_at', None)

        if title:
           return queryset.filter(title__icontains=title.lower())
        
        if published_at:
           return queryset.filter(published_at__icontains=published_at)

        return queryset

@api_view(["GET"])
def books_view(request):
    books = Book.objects.all()
    q = request.query_params.get('q', None)

    if q:
        books = books.filter(title__icontains=q)

    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, 200)