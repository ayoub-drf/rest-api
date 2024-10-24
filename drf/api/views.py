from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import throttle_classes
from rest_framework.parsers import MultiPartParser



from products.serializers import ProductSerializer
from products.models import Product
from .throttling import TenPerDayUserThrottle, ThreePerDayAnonThrottle



# Start function view

@api_view(['GET', 'POST', 'PUT', 'DELETE', ])
def index(request, pk=None):
    # print(request.content_type)
    # print(request.data)
    # print(request.method)
    # print(request.stream)
    # print(request.session.get('csrftoken'))

    if request.method == 'GET':
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({} ,status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        # r = Response()
        # r['data'] = serializer.data
        # r['status'] = status.HTTP_200_OK
        r = Response(serializer.data, status=status.HTTP_200_OK)
        # print(r.status_code)
        return r

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({} ,status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({} ,status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Start function view



# Start Throttling

@api_view(['GET'])
@throttle_classes([TenPerDayUserThrottle, ThreePerDayAnonThrottle])
def throttle_view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})

class ThrottleView(APIView):
    throttle_classes = [TenPerDayUserThrottle, ThreePerDayAnonThrottle]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello for today! See you tomorrow!"})

# End Throttling




# Start MultiPartParser data

@api_view(['POST'])
@parser_classes([MultiPartParser])
def image_receiver_view(request):
    alt = request.data.get('alt')
    img = request.data.get('img')

    if not alt:
        return Response({'err': 'alt is required'},  status=status.HTTP_400_BAD_REQUEST)
    
    if alt and img:
        return Response({'IMAGE': img.name, 'alt': alt})
    
    return Response({'err': 'Invalid/Missing DATA'}, status=status.HTTP_400_BAD_REQUEST)

# End MultiPartParser data



