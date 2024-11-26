from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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
    GenericAPIView,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
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
from .mixins import MultipleLookUPFiledMixin


from rest_framework.parsers import (
    FormParser,
    JSONParser,
    MultiPartParser,
    FileUploadParser,
)

import os

class ParserView(APIView):
    # text/plain key: value
    # parser_classes = [CustomKeyValueParser]

    # application/x-www-form-urlencoded
    # parser_classes = [FormParser]

    # application/json
    # parser_classes = [JSONParser, CustomJsonParser] 

    # application/form-data
    # parser_classes = [MultiPartParser]

    # application/form-data
    parser_classes = [FileUploadParser]

    def put(self, request, filename, *args, **kwargs):
        file = request.data['file']
        folder_path = "C:/Users/x/dev/rest-api/drf/media/upload"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_path = os.path.join("C:/Users/x/dev/rest-api/drf/media/upload/", file.name)

        if os.path.exists(save_path):
            return Response({'error': 'File already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        with open(save_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return Response({'file_name': file.name, 'file_size': file.size, "message": f'Uploaded successfully in {save_path}'})

    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     img = request.data['image']

        # with open(save_path, 'wb') as image:
        #     for chunk in img.chunks():
        #         image.write(chunk)

        # return Response({"message": "Success"})



class ProductMixinRetrieveAPIView(MultipleLookUPFiledMixin ,RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    lookup_fields = ['pk', 'name']

    def check_object_permissions(self, request, obj):
        print(self.get_permissions())
        print(self.h())
        return super().check_object_permissions(request, obj)



# Start Mixins
class ProductAPIMixinsView(GenericAPIView, ListModelMixin,
                            RetrieveModelMixin, CreateModelMixin,
                            DestroyModelMixin, UpdateModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return Product.objects.all().order_by('name')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        if pk:
            return self.retrieve(request, *args, **kwargs)
        
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# End Mixins


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



    # def get_serializer_context(self):
    #     context = super().get_serializer_context()

    #     if self.request.method == 'POST' and 'name' in context:
    #         context['name'] = context['name'].upper()


    #     return context



class ProductRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    # pagination_class = CustomPagination
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class  = ProductFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['name', 'price']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    # def filter_queryset(self, queryset):
    #     name = self.request.query_params.get('name', None)
    #     if name:
    #         return queryset.filter(name__icontains=name)
    #     return queryset

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
        # print(self.check_object_permissions(self.request, obj))

        return obj
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print('instance', instance)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        request.data['price'] = float(request.data['price']) - 10
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = 'No Content For this product'

        instance.save()
        return instance


class ProductUpdateAPIView(UpdateAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'product_id'

    def get_serializer_class(self):
        return ProductSerializer
    def get_queryset(self):
        return Product.objects.all()
    
    def update(self, request, *args, **kwargs):
        user = User.objects.get(username='maria')
        request.data['user'] = user.pk
        return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        instance = serializer.save()

        instance.name = "You can't update because I want that"
        user = User.objects.get(username='maria')

        if instance.content:
            instance.content = instance.user.email

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










