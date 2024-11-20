from rest_framework import serializers

from .models import Note


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_staff'] = user.is_staff

        return token
    
    

class NoteAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'