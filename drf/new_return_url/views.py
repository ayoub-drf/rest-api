from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.timezone import now

class SingleAPIView(APIView):
    def get(self, request, *args, **kwargs):

        return Response({'message': 'hello'}, 200)

class SimpleAPIView(APIView):
    # reverse = resolve immediately 
    # reverse = resolve later for redirect staff & success 
    def get(self, request, *args, **kwargs):
        year = 2023
        data = {
            'single': reverse('single', args=[year], request=request),
            'single_lazy': reverse_lazy('single', args=[year], request=request)
        }

        return Response(data, 200)