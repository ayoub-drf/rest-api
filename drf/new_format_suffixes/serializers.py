from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    stock = serializers.IntegerField()
    title = serializers.CharField()
    published_at = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    categories = CategorySerializer()