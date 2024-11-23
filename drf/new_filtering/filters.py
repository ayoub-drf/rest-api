from rest_framework.filters import BaseFilterBackend
import django_filters
from .models import Book

class CustomTitleBaseFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        q = request.GET.get('q').lower()
        
        return queryset.filter(title__icontains=q)
    
class BookFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('title', 'title'),
        )
    )
    out_of_stock = django_filters.BooleanFilter(method="filter_out_of_stock")

    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    categories = django_filters.CharFilter(field_name='categories__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['min_price', 'max_price', 'categories', 'out_of_stock']

    def filter_out_of_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock=0)
        
        return queryset.exclude(stock=0)