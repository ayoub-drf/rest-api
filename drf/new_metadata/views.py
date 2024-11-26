from rest_framework.generics import ListAPIView
from rest_framework.metadata import (
    SimpleMetadata,
    BaseMetadata
)

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Manager
from .serializers import (
    ManagerSerializer
)

class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description()
        }
    


class ManagerListAPIView(ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    metadata_class = MinimalMetadata