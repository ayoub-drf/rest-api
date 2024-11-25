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
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3 # Default size of instances (for example 3 products)
    max_page_size = 10
    page_query_param = 'page_number'

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
    ordering = '-pk' # Default ("-created") be aware of this also (should unchanging value) like create or id nearly unique
    template = None

# class ProductAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     def get(self, request, *args, **kwargs):
#         paginator = CustomPageNumberPagination()
#         result_page = paginator.paginate_queryset(self.get_queryset(), request)
#         serializer = ProductSerializer(result_page, many=True)

#         return paginator.get_paginated_response(serializer.data)

class CustomBasePagination(BasePagination):
    def get_count(self):
        print(self.get_queryset())
        return 10

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size', 3)

        try:
            page_size = int(page_size)
            if page_size <= 0:
                raise ValueError
            
        except ValueError:
            print("Page size must be greater then 0")
            page_size = 3
        except TypeError:
            print("Page size must be a number")
            page_size = 3

        return page_size
    
    def get_page_number(self, request):
        page_number = request.query_params.get('page_number', 1)

        try:
            page_number = int(page_number)
            if page_number <= 0:
                raise ValueError
            
        except ValueError:
            print("Page size must be greater then 0")
            page_number = 1
        except TypeError:
            print("Page size must be a number")
            page_number = 1

        return page_number
    
    def paginate_queryset(self, queryset, request, view=None): 
        page_size = self.get_page_size(request=request)
        page_number = self.get_page_number(request=request)
        # start_index = (page_size * page_number) - page_size
        # end_index = (page_size * page_number)
        
        return queryset[(page_size * page_number) - page_size:(page_size * page_number)]
    

    def get_paginated_response(self, data):
        return Response({
            "count": 11,
            "next": "self.get_next_link()",
            "previous": None,
            'results': data,
        })

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomBasePagination

class ProductListAPIViewTwo(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    