from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import NoteAPISerializer
from .models import Note



class NoteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        notes = Note.objects.all()
        serializer = NoteAPISerializer(notes, many=True)

        return Response(serializer.data)