from rest_framework import serializers
from django.contrib.auth.models import User


from books.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['profile', 'username', 'email', 'password']
        # exclude = ['password', 'id']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)

        instance.save()

        profile.name = validated_data.get('name', profile.name)
        profile.user = validated_data.get('user', profile.user)
        profile.file = validated_data.get('file', profile.file)

        profile.save()
        

        return instance