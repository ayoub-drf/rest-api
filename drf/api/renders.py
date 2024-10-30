from rest_framework.renderers import (
    JSONRenderer,
    TemplateHTMLRenderer,
    StaticHTMLRenderer,
    AdminRenderer,
    HTMLFormRenderer,
    MultiPartRenderer,
    BaseRenderer
)

from products.models import Product
from products.serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, render
from django.utils.encoding import smart_str
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import JSONParser
from http import HTTPMethod, HTTPStatus
import json

from .parsers import CustomKeyValueParser


class CustomJsonRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps(data)
    
class CustomTextPlainRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return str(data, encoding=self.charset)
    

@api_view([HTTPMethod.POST])
@renderer_classes([CustomTextPlainRenderer])
@parser_classes([CustomKeyValueParser])
def plain_text_view(request):
    data = request.data

    return Response({'msg from plain': data}, HTTPStatus.CREATED)


@api_view([HTTPMethod.POST])
@renderer_classes([CustomJsonRenderer])
@parser_classes([JSONParser])
def json_view(request):

    return Response({'msg': request.data}, HTTPStatus.CREATED)

class AdminRendererAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [AdminRenderer]  

@api_view([HTTPMethod.GET])
@renderer_classes([StaticHTMLRenderer])
def static_html_renderer_view(request):
    product = get_object_or_404(Product, pk=1)
    
    html = f"""
        <h1>{product.uuid}</h1>
    """
    return Response(html)

@api_view([HTTPMethod.GET])
@renderer_classes([JSONRenderer])
def json_render_view(request):
    products = Product.objects.all().order_by('-published')
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data, HTTPStatus.OK)


class TemplateHTMLRendererAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, product_id=None):
        if product_id:            
            product = get_object_or_404(Product, pk=product_id)
            serializer = ProductSerializer(product)

            return Response({'product': serializer.data}, template_name='products/get.html')

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response({'products': serializer.data}, template_name='products/list.html')


