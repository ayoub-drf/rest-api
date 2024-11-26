books = [
    {
        "id": 6,
        "stock": 2,
        "title": "Clothing 1",
        "published_at": 2020,
        "price": "22.99",
        "categories": {
            "name": "shoes"
        }
    },
    {
        "id": 7,
        "stock": 0,
        "title": "Clothing 2",
        "published_at": 2020,
        "price": "92.99",
        "categories": {
            "name": "shoes"
        }
    },
    {
        "id": 8,
        "stock": 2,
        "title": "Clothing 3",
        "published_at": 2021,
        "price": "22.99",
        "categories": {
            "name": "shoes"
        }
    },
    {
        "id": 9,
        "stock": 2,
        "title": "phone 1",
        "published_at": 2022,
        "price": "22.99",
        "categories": {
            "name": "phones"
        }
    },
    {
        "id": 10,
        "stock": 2,
        "title": "phone 2",
        "published_at": 2020,
        "price": "922.99",
        "categories": {
            "name": "phones"
        }
    },
    {
        "id": 11,
        "stock": 0,
        "title": "phone 3",
        "published_at": 2021,
        "price": "123.02",
        "categories": {
            "name": "phones"
        }
    }
]

from .serializers import BookSerializer

from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, parser_classes, api_view

from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer

from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

# You can also use the query format 
# http://127.0.0.1:8000/books?format=xml

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer, YAMLRenderer, XMLRenderer])
@parser_classes([MultiPartParser, JSONParser, YAMLParser, XMLParser])
def book_view(request, format=None): # Format required
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, 200)


class Books(ListAPIView):
    queryset = books
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, JSONParser, YAMLParser, XMLParser)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, YAMLRenderer, XMLRenderer)
