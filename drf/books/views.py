from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from http import HTTPStatus, HTTPMethod
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from .serializers import (
    PersonSerializer,
    BookSerializer,
)
from .models import (
    Book
)

User = get_user_model()



class UserAPIView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def put(self, request, pk=None, *args, **kwargs):
        data = request.data
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@api_view([HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH])
def home(request, pk=None):
    if request.method == HTTPMethod.POST:
        data = request.data
        serializer = BookSerializer(data=data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            serializer.save(user=request.user)

        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)
    
    if request.method == HTTPMethod.PUT:
        data = request.data
        book = get_object_or_404(Book, pk=pk)

        serializer = BookSerializer(book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.OK)
    
    if request.method == HTTPMethod.PATCH:
        data = request.data
        book = get_object_or_404(Book, pk=pk)

        serializer = BookSerializer(book, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.OK)


    if pk:
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


    books = Book.objects.all().order_by('-created')
    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, HTTPStatus.OK)