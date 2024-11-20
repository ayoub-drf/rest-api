from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer
from http import HTTPMethod, HTTPStatus

@api_view(['GET'])
def api(request):
    serializer = NoteSerializer(Note.objects.all(), many=True)

    return Response(serializer.data, HTTPStatus.OK)