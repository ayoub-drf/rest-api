from rest_framework import serializers

from .models import (
    Album,
    Track,
    Publisher,
    Author,
    Book,
    Library,
)

from django.shortcuts import get_object_or_404
from django.urls import reverse


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    # StringRelatedField refer to the __str__
    # author = serializers.StringRelatedField()
    # publisher = serializers.StringRelatedField()

    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Book
        fields = ('id', 'title', "author", 'publisher')

class CustomPrimaryKeyRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.pk
    
    
    def to_internal_value(self, data):
        try:
            book = Book.objects.get(pk=data)
            return book.pk
        except Exception as e:
            raise serializers.ValidationError(f"Invalid Input: ({e})")


class CustomHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = "book-detail"
    queryset = Book.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.pk
        }
        url = request.build_absolute_uri(reverse(view_name, kwargs=url_kwargs))
        
        return url
    
    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


class LibrarySerializer(serializers.ModelSerializer):
    # books = CustomHyperLinkedRelatedField(many=True)
    books = CustomPrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)
    # library = serializers.HyperlinkedIdentityField(
    #     view_name="libraries-detail",
    #     read_only=True
    # )
    # books = BookSerializer(many=True)
    # books = serializers.StringRelatedField(many=True)
    # books = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Book.objects.all(),
    # )
    # books = serializers.HyperlinkedRelatedField(
    #     queryset=Book.objects.all(),
    #     many=True,
    #     view_name="book-detail",
    #     # read_only=True,
    #     # allow_null=True,
    #     lookup_field="pk",
    #     lookup_url_kwarg="pk",
    # )
    # books = serializers.SlugRelatedField(
    #     queryset=Book.objects.all(),
    #     many=True,
    #     # view_name="book-detail",
    #     slug_field="slug"
    # )
    # books = serializers.HyperlinkedIdentityField(
    #     view_name="book-detail",
    #     many=True,
    #     lookup_field="pk",
    #     lookup_url_kwarg="pk",
    # )

    # books = BookSerializer(many=True)


    class Meta:
        model = Library
        fields = ('name', "books")


class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(
            many=True,
            read_only=True,
            # slug_field='title'
        )
    class Meta:
        model = Album
        fields = ('id', 'album_name', "artist", "tracks")


