from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import throttle_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView, 
)

from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import django_filters
from django_filters.rest_framework import DjangoFilterBackend


from products.serializers import ProductSerializer
from products.models import Product
from .throttling import TenPerDayUserThrottle, ThreePerDayAnonThrottle
from .pagination import CustomPagination
from .mails import send_email_confirmation


# Start Django Filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # For name filtering

    class Meta:
        model = Product
        fields = ['name', ]

# End Django Filters




# Start Generics Views

class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class  = ProductFilter

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name', None)
        if name:
            return queryset.filter(name__icontains=name)
        return queryset

    # def get_queryset(self):
    #     return Product.objects.filter(name__icontains='product')
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

custom_list_api_view = ProductListAPIView.as_view()


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'
    # multiple_lookup_fields = ['pk', 'color']
    # multiple_lookup_url_kwarg = ['id', 'color_name']
    

    def get_object(self):
        pk = self.kwargs['pk']
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)

        print(self.check_object_permissions(self.request, obj))

        return obj


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        user = User.objects.get(username='maria')

        send_email_confirmation(user=user, modified=instance)
        
        instance.user = user
        if not instance.content:
            instance.content = user.email

        instance.save()

        return instance


class ProductUpdateAPIView(UpdateAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'product_id'

    def get_serializer_class(self):
        return ProductSerializer
    def get_queryset(self):
        return Product.objects.all()
    
    def perform_update(self, serializer):
        instance = serializer.save()

        instance.name = "You can't update because I want that"

        if not instance.content:
            instance.content = self.request.user.email

        instance.save()

        return instance


class ProductDestroyAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        name = instance.name
        return Response({f'{name}': 'has been deleted'}, status=status.HTTP_200_OK)


# End Generics Views




# Start function view

@api_view(['GET', 'POST', 'PUT', 'DELETE', ])
def index(request, pk=None):
    # print(request.content_type)
    # print(request.data)
    # print(request.method)
    # print(request.stream)
    # print(request.session.get('csrftoken'))

    if request.method == 'GET':
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({} ,status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        # r = Response()
        # r['data'] = serializer.data
        # r['status'] = status.HTTP_200_OK
        r = Response(serializer.data, status=status.HTTP_200_OK)
        # print(r.status_code)
        return r

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({} ,status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({} ,status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Start function view




# Start API View

class CustomAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({'err': 'Product does not exists'})
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        name = request.query_params.get('name', None)
        price = request.query_params.get('price', None)

        if name:
            products = Product.objects.filter(name__icontains=name)

        if price:
            products = Product.objects.filter(price__icontains=price)

        if price and name:
            products = Product.objects.filter(Q(price__icontains=price) | Q(name__icontains=name))

            
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({} ,status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({} ,status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# Start API View




# Start Throttling

@api_view(['GET'])
@throttle_classes([TenPerDayUserThrottle, ThreePerDayAnonThrottle])
def throttle_view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})

class ThrottleView(APIView):
    throttle_classes = [TenPerDayUserThrottle, ThreePerDayAnonThrottle]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello for today! See you tomorrow!"})

# End Throttling




# Start MultiPartParser data

@api_view(['POST'])
@parser_classes([MultiPartParser])
def image_receiver_view(request):
    alt = request.data.get('alt')
    img = request.data.get('img')

    if not alt:
        return Response({'err': 'alt is required'},  status=status.HTTP_400_BAD_REQUEST)
    
    if alt and img:
        return Response({'IMAGE': img.name, 'alt': alt})
    
    return Response({'err': 'Invalid/Missing DATA'}, status=status.HTTP_400_BAD_REQUEST)

# End MultiPartParser data



