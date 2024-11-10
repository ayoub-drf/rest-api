from rest_framework import serializers
from .models import Book
from django.urls import reverse

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    age = serializers.IntegerField()

    def validate_name(self, value):
        if value.lower() == 'james':
            raise serializers.ValidationError('name can not be james')
        
        return value
    
    def validate(self, attrs):
        age = attrs['age']
        if age < 20:
            raise serializers.ValidationError('Age must be greater then 19')
        
        return attrs

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    id = serializers.IntegerField()
    is_staff = serializers.BooleanField()


class BookSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(required=False)

    class Meta:
        model = Book
        fields = ['url', 'id', 'name', 'price', 'created', 'user']

    def get_url(self, obj):
        request = self.context.get('request')
        url = reverse(viewname='product_detail', kwargs={'pk': obj.pk})
        if request:
            return request.build_absolute_uri(url)
                
        return url

    
    def validate_name(self, value):
        if value.lower() == 'james':
            raise serializers.ValidationError('name can not be james')
        
        return value
    
    def create(self, validated_data):
        validated_data['name'] = validated_data.pop('name').upper()
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()

        instance.save()
        return instance


    def save(self, **kwargs):            
        name = self.validated_data['name']
        name.upper()

        print(kwargs)

        
        return super().save(**kwargs)
