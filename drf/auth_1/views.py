from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from http import HTTPMethod, HTTPStatus

from .serializers import (
    Auth1Serializers,
    RegisterSerializer,
)
from .authentication import CustomTokenAuthentication, APIKeyAuthentication

class SampleView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated successfully!"})


@api_view([HTTPMethod.POST, HTTPMethod.GET])
def register_1(request):
    if request.method == 'POST':
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)




@api_view([HTTPMethod.POST, HTTPMethod.GET])
@authentication_classes([BasicAuthentication, SessionAuthentication, CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def auth_1(request):
    # print("request.auth", request.auth)
    
    data = [
        {'username': "dexter"},
    ]
    serializer = Auth1Serializers(data, many=True)

    return Response(serializer.data, HTTPStatus.OK)


