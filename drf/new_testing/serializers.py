from rest_framework import serializers

from .models import (
    Post
)

class PostSerializerTwo(serializers.Serializer):
    name = serializers.CharField(min_length=10)

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="author.username", required=False)
    
    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'author', 'username')
        # depth = 1
