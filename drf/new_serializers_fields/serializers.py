from rest_framework import serializers

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

import datetime
from uuid import uuid4
import os
from django.conf import settings
from django.utils import timezone
import pytz
import re
from datetime import timedelta


from .models import (
    Child,
    Product,
    Father
)
from .validators import (
    positive_number
)

class CustomSerializerTwo(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True, allow_empty_file=True)
    image = serializers.ImageField(use_url=True, max_length=100)

    class Meta:
        model = Product
        fields = "__all__"

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()


class ProductListSerializer(serializers.ListField):
    title = serializers.CharField()
    slug = serializers.SlugField()

class CustomJsonSerializer(serializers.DictField):
    name = serializers.JSONField()

class CustomCharField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, str):
            return value.upper()
    
    def to_internal_value(self, data):
        if isinstance(data, str):
            if "int" in data.lower():
                raise serializers.ValidationError('value cannot be an int')
            
            return data
        
        raise serializers.ValidationError("Must be a string")
    
class Color:
    def __init__(self, red, green, blue):
        self.red, self.green, self.blue = red, green, blue

class ColorField(serializers.Field):
    def to_representation(self, value):
        return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)

    default_error_messages = {
        'incorrect_type': 'Incorrect type. Expected a string, but got {input_type}',
        'incorrect_format': 'Incorrect format. Expected `rgb(#,#,#)`.',
        'out_of_range': 'Value out of range. Must be between 0 and 255.'
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
            self.fail('incorrect_format')

        data = data.strip('rgb(').rstrip(')')
        red, green, blue = [int(col) for col in data.split(',')]

        if any([col > 255 or col < 0 for col in (red, green, blue)]):
            self.fail('out_of_range')

        return Color(red, green, blue)

class CustomSerializerOne(serializers.Serializer):
    color = ColorField()
    is_available = serializers.BooleanField()
    name = serializers.CharField(
        min_length=5, max_length=150, trim_whitespace=True, #, Remove spaces from string ' x ' = 'x'
        allow_blank=False, # This field may not be blank.
        allow_null=False, # his field may not be null.
    )
    email = serializers.EmailField( min_length=7, max_length=150, allow_blank=False)
    reg = serializers.RegexField( regex="\d+", max_length=None, min_length=None, allow_blank=False)
    slug = serializers.SlugField(max_length=50, min_length=None, allow_blank=False)
    url = serializers.URLField(max_length=200, min_length=None, allow_blank=False)
    uuid = serializers.UUIDField(
        # format="hex", # Without hyphens
        # format="hex_verbose", # With hyphens
        # format="int", # A 128 bit integer representation
        format="urn", # RFC 4122 URN representation
        default=uuid4, read_only=True
    ) 
    image_path = serializers.FilePathField(
        path=os.path.join(settings.BASE_DIR, "media"),
        match=r'.*\.png$',
        recursive=True,  # Allow files in subdirectories
        allow_files=True,  # Allow files (default)
        allow_folders=False  # Do not allow directories
    )
    ip = serializers.IPAddressField(
        protocol="both", # Accept IPv4 & IPv6
        # protocol="ipv4", # Accept Only IPv4
        # protocol="ipv6", # Accept Only IPv6
    )
    integer_field = serializers.IntegerField(max_value=10, min_value=1)
    float_field = serializers.FloatField(max_value=10.0, min_value=1.0)
    decimal_field = serializers.DecimalField(
        max_digits=5, decimal_places=2,
        max_value=999.99 , min_value=111.00,
        coerce_to_string=False # If False return an integer for representation or True == string
    )
    event_datetime = serializers.DateTimeField(
        # format="%Y-%m-%d %H:%M:%S", # One datetime format (this response)
        input_formats=["%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"], # multiple datetime formats
        # default_timezone=pytz.utc,
    )
    event_date = serializers.DateField(input_formats=["%Y-%m-%d", "%Y/%m/%d"])
    event_time = serializers.TimeField(format="%H-%M-%S", input_formats=["%H-%M-%S", "%H:%M:%S"])
    event_duration = serializers.DurationField(
        min_value=timedelta(minutes=1, seconds=10),
        max_value=timedelta(minutes=5, seconds=10),
    )
    single_status = serializers.ChoiceField(choices=[
            ('admin', 'Admin'),
            ('editor', 'Editor'),
        ],
        # allow_blank=True,
    )
    multiple_choice = serializers.MultipleChoiceField(
        choices=[
            ('admin', 'Admin'),
            ('editor', 'Editor'),
            ('viewer', 'Viewer'),
        ]
    )
    names = serializers.ListField(
        child=serializers.CharField(min_length=2),
        allow_empty=True,
        # min_length=2,
        # max_length=2
    )
    person = serializers.ListField(
        child=PersonSerializer()
    )
    product = ProductListSerializer()
    my_dict = serializers.DictField(
        child=serializers.CharField()
    )
    my_dict_json = CustomJsonSerializer()
    my_json = serializers.JSONField(binary=False) # If Binary True will treat the data as json not as python primitive type

    x = serializers.ReadOnlyField(default="Hello world my name is dexter")
    # modified = serializers.HiddenField(default=timezone.now)
    time_now = serializers.SerializerMethodField()
    custom_name = CustomCharField()

    def create(self, validated_data):
        return validated_data
    
    def get_time_now(self, obj):
        return datetime.datetime.now()






class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(style={'input_type': 'password'})
    favorite_color = serializers.ChoiceField(
        choices=['red', 'green', 'blue'],
        style={'base_template': 'radio.html'}
    )
    bio = serializers.CharField(
        style={'input_type': 'textarea', 'rows': 5, 'border': "1px solid red"},
        required=False
    )

class ChildModelViewSetSerialize(serializers.ModelSerializer):
    name = serializers.CharField(
                label='your name',
                help_text='write your name',
                style={
                    'input_type': 'mama',
                    }
                )
    
    day = serializers.DateField(initial="12/02/2002")

    class Meta:
        model = Child
        fields = '__all__'

    # def get_day(self, obj):
    #     return ''

class ChildSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(source="father.email")
    # obj_it_self = serializers.CharField(source="*")

    class Meta:
        model = Child
        fields = ('id', 'name', 'username')

class Home1Serializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    help_text = serializers.CharField(allow_null=True)
    name = serializers.CharField(min_length=2, max_length=10, default='Guest')
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, write_only=True)
    username = serializers.CharField(
        validators=[MaxLengthValidator(10, "The value must be less then 10 characters"), MinLengthValidator(5, "The value must be at least 5 characters")]
    )
    price = serializers.IntegerField(validators=[positive_number])
    number = serializers.CharField(validators=[RegexValidator(r'^\+?1?\s?\d{9,15}$', "Invalid Number")])
    work_name = serializers.CharField(
        max_length=20, error_messages={
            'required': 'The name field cannot be empty.',
            'max_length': 'Name cannot be more than 20 characters.'
        }
    )

    
    def validate(self, attrs):
        # name = attrs.get('name', '')
        # if name == "james":
        #     raise serializers.ValidationError({'name': 'Invalid Name'})

        return attrs
    
    def create(self, validated_data):
        name = validated_data['name']
        validated_data['name'] = name.upper()

        return validated_data
    
    def to_representation(self, instance):
        password = instance.pop('password')

        return instance
