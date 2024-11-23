from rest_framework.pagination import (
    BasePagination,
    CursorPagination,
    LimitOffsetPagination,
    DjangoPaginator,
    InvalidPage,
    NotFound,
    PageNumberPagination,
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 4 # Default size of instances (for example 3 products)
    max_page_size = 10
    page_query_param = 'q'

     # ?q=1&page_size=2 # for overriding the (page_size) and query your own (page_size=2)
    page_size_query_param = 'page_size' # The maximum number must be less or equal 10 (max_page_size)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    # ?offset=3&limit=4
    default_limit = 2 # The default results
    max_limit = 6 # The maximum results if you specified a [(?limit=5) means 6 result instead of the default]
    limit_query_param = "limit" # default
    offset_query_param  = "offset" # default
    template = None


class CustomCursorPagination(CursorPagination):
    page_size = 2
    ordering = '-pk'
    template = None

# class ProductAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     def get(self, request, *args, **kwargs):
#         paginator = CustomPageNumberPagination()
#         result_page = paginator.paginate_queryset(self.get_queryset(), request)
#         serializer = ProductSerializer(result_page, many=True)

#         return paginator.get_paginated_response(serializer.data)

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = (CustomCursorPagination )
    