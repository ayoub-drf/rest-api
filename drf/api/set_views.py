from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from products.models import Product
from products.serializers import ProductSerializer


# Start ViewSet

class ProductListRetrieveViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data)
    
    def create(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def delete(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        product.delete()

        return Response({'status': f'Product {product.name} has been deleted'})
    
    def put(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
# product_list = ProductListRetrieveViewSet.as_view({'get': 'list'})
# product_retrieve = ProductListRetrieveViewSet.as_view({'get': 'retrieve'})
# product_create = ProductListRetrieveViewSet.as_view({'post': 'create'})
# product_delete = ProductListRetrieveViewSet.as_view({'delete': 'delete'})
# End ViewSet


