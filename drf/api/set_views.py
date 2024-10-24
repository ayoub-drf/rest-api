from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import UserSerializer


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



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    basename = 'user'
    description = "This viewset provides CRUD operations for user."
    permission_classes = None


    @action(detail=True, methods=['get'], url_path=r'products')
    def get_user_products(self, request, pk=None):
        user = self.get_object()
        products = user.product_set.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


