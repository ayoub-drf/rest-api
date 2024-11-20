from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

class Auth1Serializers(serializers.Serializer):
    username = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', "password"]

    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        token = Token.objects.create(user=user)
        return {'Token': f"{token}"}
    
    def to_representation(self, instance):
        return instance