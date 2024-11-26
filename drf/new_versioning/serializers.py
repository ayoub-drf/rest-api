from rest_framework import serializers

class CustomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()