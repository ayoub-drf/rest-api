from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView

from django.contrib.auth.models import User

from .serializers import (
    CustomSerializer,
    BookSerializer
)
from .models import (
    Book
)

class BookCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET', 'POST'])
def index_1(request):
    if request.method == 'POST':
        data = request.data
        serializer = CustomSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    data = [
        {'email': "x@aol.com"},
    ]
    serializer = CustomSerializer(data, many=True)
    print(serializer.data)
    return Response(serializer.data)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView

from django.contrib.auth.models import User

from .serializers import (
    CustomSerializer,
    BookSerializer,
    EventSerializer,
)
from .models import (
    Book,
    Event,
)

class EventCreateAPIView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class BookCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET', 'POST'])
def index_1(request):
    if request.method == 'POST':
        data = request.data
        serializer = CustomSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    data = [
        {'id': request.user.pk},
    ]
    serializer = CustomSerializer(data, many=True)
    print(serializer.data)
    return Response(serializer.data)