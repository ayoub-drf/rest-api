from rest_framework import serializers

from .models import Book, Category


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

class BookSerializer(serializers.ModelSerializer):
    categories = BookSerializer()
    class Meta:
        model = Book
        fields = ('id', 'stock', 'title', 'published_at', 'price', 'categories')