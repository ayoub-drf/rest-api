from rest_framework import serializers
from .models import Product
from django_filters.rest_framework import filters

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'