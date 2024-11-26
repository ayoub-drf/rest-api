from rest_framework import serializers
from rest_framework.validators import (
    UniqueValidator,
    UniqueTogetherValidator,
    UniqueForDateValidator,
    UniqueForMonthValidator,
    UniqueForYearValidator,
)

from rest_framework.fields import (
    CreateOnlyDefault,
    ReadOnlyField,
    CurrentUserDefault,
)

from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Book,
    Event,
)


class EventSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, default=CreateOnlyDefault(CurrentUserDefault()))
    created_at = serializers.DateTimeField(default=CreateOnlyDefault(timezone.now))

    class Meta:
        model = Event
        fields = "__all__"
        validators = [
            # UniqueForDateValidator( # For the entire date
            #     queryset=Event.objects.all(),
            #     field='location',
            #     date_field="date"
            # ),
            # UniqueForMonthValidator( # For just the month
            #     queryset=Event.objects.all(),
            #     field='location',
            #     date_field="date"
            # ),
            UniqueForYearValidator( # For just the month
                queryset=Event.objects.all(),
                field='location',
                date_field="date"
            )
        ]
        # validators = []  # Disable the default validators

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['name', 'order'],
                message="One of the two should be unique :)")
        ]

class CustomSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        # validators=[
        #     UniqueValidator(
        #         queryset=User.objects.all(),
        #         message="This email already exists :)",
        #         lookup='exact'
        #     )
        # ]
    )