from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    AuthenticationFailed,
    ErrorDetail,
    MethodNotAllowed,
    NotAcceptable,
    NotAuthenticated,
    PermissionDenied,
    ParseError,
    UnsupportedMediaType,
    Throttled,
)

# NotFound,             # 404 - Resource not found
# ValidationError,      # 400 - Invalid input data
# APIException,         # General custom exception
# AuthenticationFailed, # 401 - Authentication failure
# ErrorDetail,          # Detailed error message (used with exceptions)
# MethodNotAllowed,     # 405 - HTTP method not allowed
# NotAcceptable,        # 406 - Not acceptable request
# NotAuthenticated,     # 401 - Not authenticated
# PermissionDenied,     # 403 - Permission denied
# ParseError,           # 400 - Parse error in request
# UnsupportedMediaType, # 415 - Unsupported media type
# Throttled,            # 429 - Rate limiting (too many requests)

from django.shortcuts import get_object_or_404



from .models import Book
from .serializers import BookSerializer
from .exceptions import (
    CustomValidatorNameException
)

class CustomAnonRateThrottle(AnonRateThrottle):
    anon = '1/day'



class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            # book = get_object_or_404(Book, pk=pk)
            # serializer = BookSerializer(book)
            # return Response(serializer.data)
            try:
                book = Book.objects.get(pk=pk)
                serializer = BookSerializer(book)
                return Response(serializer.data)
            except Book.DoesNotExist:
                raise NotFound(f"the book with this {pk} was not found")
                # raise ValidationError({'Not found': f"the book with this {pk} was not found"}, 404)

        else:
            # return Response({'detail': f"invalid pk {pk}"}, 400)
            raise ValidationError({'detail': f"invalid pk {pk}"}, 400)
        
    def post(self, request):
        data = request.data
        if 'name' not in data:
            raise ValidationError({'name': ErrorDetail("This field is required./", code="required")}, 400)
            # raise ValidationError({'name': "This field is required"}, 400)
            # raise CustomValidatorNameException()
        
    
        return Response()



class ProtectedView(APIView):
    throttle_classes = (CustomAnonRateThrottle, )
    def get(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated("Authentication credentials were not provided.", 401)
        
        if "application/json" not in request.headers.get("Accept"):
            raise NotAcceptable("{Accept: application/json} is missing")
        
        if not request.user.is_staff:
            raise PermissionDenied("You do not have the staff permission")
        
        return Response({"message": "You have access!"})
    
    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")
    
    def put(self, request, *args, **kwargs):
        # try:
        #     data = request.data
        # except Exception as e:
        #     raise ParseError("Accept only json data")

        # if request.content_type != "application/xml":
        #     raise UnsupportedMediaType("Accept only application/xml")

        return Response({"message": "Passed"})
    
    def throttled(self, request, wait):
        raise Throttled(detail={
              "message":"You have exceeded your request limit.",
              "availableIn":f"{int(wait)} seconds",
              "throttleType":"anon"
        })
        
