from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from http import HTTPMethod, HTTPStatus
from datetime import timedelta

from .serializers import (
    Home1Serializer,
    ChildSerializer,
    CustomSerializerOne,
    CustomSerializerTwo,
)
from .models import (
    Child,
    Product,
)

@api_view([HTTPMethod.POST, HTTPMethod.GET])
def custom_serializer_two_view(request):
    if request.method == HTTPMethod.POST:
        data = request.data
        serializer = CustomSerializerTwo(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTPStatus.CREATED)


    data = Product.objects.all()
    serializer = CustomSerializerTwo(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    
    return Response(serializer.data, HTTPStatus.OK)


@api_view([HTTPMethod.POST, HTTPMethod.GET])
def custom_serializer_one_view(request):
    if request.method == HTTPMethod.POST:
        serializer = CustomSerializerOne(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)
    
    data = [
        {
            'is_available': True, "name": "James", "email": "x@aol.com",
            "reg": "2", "slug": "slug-field", "url": "https://a.com",
            "image_path": r"C:\Users\x\dev\rest-api\drf\media\default_img.png",
            "ip": "::ffff:192.168.1.1", "integer_field": 10, "float_field": 10.0,
            "decimal_field": 122.00, "event_datetime": "2024-11-09 06:25:28",
            "event_date": "2024/11/09", "event_time": "06-25-28",
            "event_duration": timedelta(minutes=5, seconds=8),
            "single_status": "admin", "multiple_choice": ["admin", "viewer"],
            "names": [], "person": [{"name": "James", "age": 33}, {"name": "dexter", "age": 33}],
            "product": [{"title": "product 1", "slug": "product-1"}, {"title": "product 2", "slug": "product-2"}],
            "my_dict": {"name": "James", "age": 33}, "my_dict_json": {"x": {'title': "James"}},
            "my_json": {
                'preferences': {
                    'notifications': {'email': True, 'sms': False},
                    'languages': ['English', 'Spanish']
                }
            },
            "email_m": "x@aol.com",
            "custom_name": "Dexter",
        }
    ]
    serializer = CustomSerializerOne(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, HTTPStatus.OK)






@api_view([HTTPMethod.POST, HTTPMethod.GET])
def home_2(request):
    if request.method == HTTPMethod.POST:
        pass
        

    data = Child.objects.all()
    serializer = ChildSerializer(data, many=True)

    return Response(serializer.data, HTTPStatus.OK)


@api_view([HTTPMethod.POST, HTTPMethod.GET])
def home_1(request):
    if request.method == HTTPMethod.POST:
        data = request.data
        serializer = Home1Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)
        

    data = [
        {
            'name': "james",
            "price": 20, 
            "username": "dexter",
            'help_text': None,
            "email": "x@aol.com",
            "password": "password123",
            "number": "+1898893988",
            "work_name": "james_clear"

        },
    ]
    
    serializer = Home1Serializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, HTTPStatus.OK)