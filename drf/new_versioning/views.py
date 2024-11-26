from rest_framework.versioning import (
    AcceptHeaderVersioning,
    QueryParameterVersioning,
    URLPathVersioning,
    NamespaceVersioning,
)



from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from http import HTTPMethod, HTTPStatus

from .serializers import (
    CustomSerializer
)

class CustomQueryParameterVersioning(QueryParameterVersioning):
    default_version = None
    version_param = "ver"

class PersonsListAPIView(ListAPIView):
    serializer_class = CustomSerializer
    queryset = [
            {'id': 1, 'username': "james"},
            {'id': 2, 'username': "dexter"},
            {'id': 3, 'username': "maria"},
        ]
    versioning_class = CustomQueryParameterVersioning

    def get_queryset(self):
        queryset = self.queryset
        if self.request.version == "1":
            return queryset[1:2]
        return queryset


@api_view([HTTPMethod.GET])
def index_v1(request):
    data = {
        'v1': "view"
    }
    return Response(data=data, status=HTTPStatus.OK)

@api_view([HTTPMethod.GET])
def index_v2(request):
    data = {
        'v2': "view"
    }
    return Response(data, HTTPStatus.OK)
