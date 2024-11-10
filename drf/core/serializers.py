from rest_framework import serializers


from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import (
    UserProfile,
    Post,
    Like,
    Monitor,
    Book,
    Author,
    Customer,
    Product,
    Library,
    HighScore,
)

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None) # ['username', 'email']

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields) # allowed {'email', 'username'}
            existing = set(self.fields) # {'is_active', 'email', 'last_name', 'username', 'first_name'}
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializerTen(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']




class CustomSerializerX(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    id = serializers.IntegerField(required=False, default=1)

    class Meta:
        fields = ('id', 'name')

    def validate_name(self, value):
        if value.lower() == 'james':
            return serializers.ValidationError("Invalid name")
        return value
    
    def create(self, validated_data):
        return validated_data
    
class NameSerializer(CustomSerializerX):
    id = None
    pass




class HighScoreSerializer(serializers.BaseSerializer):
    """
        1  to_internal_value
        2   is_valid (implicitly called by DRF)
        3   save()
        4   create()
        5   to_representation
    """
    def to_internal_value(self, data):
        # player_name = data.get('player_name')
        # score = data.get('score')

        # return {
        #     'score': int(score),
        #     'player_name': player_name
        # }
        return {"msg": "Ok"}
    
    def to_representation(self, instance):
        # return {
        #     'id': instance.id,
        #     'player_name': instance.player_name,
        #     'score': instance.score,
        # }
        return {"msg": "Ok"}
    
    def create(self, validated_data):
        # return HighScore.objects.create(**validated_data)
        return {"msg": "Ok"}




class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='customers-detail', lookup_field='name', read_only=True
    )

    product = serializers.HyperlinkedRelatedField(
        view_name="products-detail",
        many=True,
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Customer
        fields = ['id', 'url', 'name', 'uuid', 'user', 'product']
        # extra_kwargs = {
        #     'url': {'view_name': 'customers-detail', 'lookup_field': 'name'}
        # }



class AuthorSerializer(serializers.ModelSerializer):
    class CustomReadOnlyFieldField(serializers.ReadOnlyField):
        def to_representation(self, value):
            return f"Author: {value}"
        
    name_in_uppercase = CustomReadOnlyFieldField()

    class CustomUrlField(serializers.URLField):
        def to_representation(self, value):
            if not value.startswith('https'):
                value = 'local url: ' + value
            return super().to_representation(value)
        
    url = CustomUrlField()

    location = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Author
        fields = ('id', 'name', 'name_in_uppercase', 'url', "location")

    def create(self, validated_data):
        location = validated_data.pop('location')
        print(location)

        return super().create(validated_data)
    


class BookSerializerTwo(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ('id', 'name', 'published', 'author')



class CustomTitleField(serializers.CharField):
    def to_representation(self, value):
        return f'The Book Title Is : {value.upper()}'
    
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError('Title must be string')
        
        if 'book' in data.lower():
            raise serializers.ValidationError('Title cannot contains book in it\' text')
        
        return data

    
class BookSerializer(serializers.Serializer):
    title = CustomTitleField(max_length=100, required=True)
    published_date = serializers.DateField()

    class Meta:
        fields = ('title', 'published_date')

    def create(self, validated_data):
        return validated_data



class MonitorSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
    ], required=True)
    
    class Meta:
        model = Monitor
        fields = ['id', 'name', 'status']



class PostSerializerFour(serializers.ModelSerializer):
    external_url = serializers.URLField()

    class Meta:
        model = Post
        fields = ('id', 'owner', 'external_url', 'created', 'content')
        # exclude = ['external_website']

class OwnerSerializerThree(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class PostSerializerThree(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )

    class Meta:
        model = Post
        fields = ['owner', 'id', 'content', 'created', 'url']

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'email']

class PostSerializerTwo(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) # To get just the id of the owner
    owner = OwnerSerializer() # To get the entire fields

    class Meta:
        model = Post
        fields = '__all__'

def not_allowed_name(value):
    if value == 'james':
        raise serializers.ValidationError('James is not allowed')

class ContactFormSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(validators=[not_allowed_name])

    def create(self, validated_data):
        self.send_email(validated_data['email'], validated_data['name'])
        return validated_data

    def send_email(self, email, name):
        letter = {
            'subject': 'An email from Django',
            'message': f'Subscribed. Thanks {name}!',
            'recipient_list': [email],
            'from_email': settings.EMAIL_HOST_USER,
        }
        send_mail(**letter)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=['content']
            )
        ]
    
    def create(self, validated_data):
        original_data = self.initial_data

        return Post.objects.create(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    # username = serializers.CharField()
    # email = serializers.EmailField()
    # password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        print(profile_data)

        user = User.objects.create(**validated_data)
        user.set_password(raw_password=validated_data['password'])

        profile = UserProfile.objects.create(user=user, **profile_data)
        user.save()

        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'userprofile'):
            representation['profile'] = UserProfileSerializer(instance.userprofile).data

        return representation
    
class LikeSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'url']
        # depth = 2


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

