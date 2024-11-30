from rest_framework import serializers
from rest_framework.serializers import (
    ValidationError,

)

from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    
    def validate_name(self, value):
        if len(value.strip()) == 0:
            raise ValidationError("name can not be blank", 400)
        return value