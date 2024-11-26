from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from http import HTTPMethod, HTTPStatus

from .models import (
    Album,
    Track,
    Library,
    Book,
)
from .serializers import (
    AlbumSerializer,
    LibrarySerializer,
    BookSerializer,
)

class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class LibraryListCreateAPIView(ListCreateAPIView):
#     queryset = Library.objects.all()
#     serializer_class = LibrarySerializer

@api_view([HTTPMethod.POST, HTTPMethod.GET])
def index_1(request, pk=None):
    if request.method == HTTPMethod.POST:
        data = request.data
        serializer = LibrarySerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    if pk:
        qs = get_object_or_404(Library, pk=pk)

        serializer = LibrarySerializer(qs)

        return JsonResponse(serializer.data, safe=False)
    
    qs = Library.objects.prefetch_related('books')

    serializer = LibrarySerializer(qs, many=True, context={"request": request})

    return Response(serializer.data)

@api_view([HTTPMethod.GET])
def index_1_single(request, pk=None):
    try:
        qs = Library.objects.get(pk=pk)
        serializer = LibrarySerializer(qs,  context={"request": request})

        return JsonResponse(serializer.data, safe=False)
    
    except Library.DoesNotExist:
        return JsonResponse(serializer.errors, safe=False) 
