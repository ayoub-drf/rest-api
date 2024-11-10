from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .serializers import (
    UserProfileSerializer,
    UserSerializer,
    PostSerializer,
    ContactFormSerializer,
    LikeSerializer,
    CreateUserSerializer,
    PostSerializerTwo,
    PostSerializerThree,
    OwnerSerializerThree,
    PostSerializerFour,
    MonitorSerializer,
    BookSerializer,
    BookSerializerTwo,
    AuthorSerializer,
    CustomerSerializer,
    ProductSerializer,
    LibrarySerializer,
    HighScoreSerializer,
    NameSerializer,
    UserSerializerTen,
)
from .models import (
    Post,
    Like,
    Monitor,
    Book,
    Author,
    Customer,
    Product,
    Library,
    HighScore,
)

from http import (
    HTTPMethod,
    HTTPStatus
)

@api_view(['GET'])
def user_api_view_ten(request):
    user = User.objects.get(username="dexter")
    serializer = UserSerializerTen(user, fields=['username', 'email'])
    # print(serializer.data)
    
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def name_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = NameSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    obj = [
        {"name": "James"},
        {"name": "Dexter"},
        {"name": "Maria"},
    ]
    serializer = NameSerializer(obj, many=True)

    return Response(serializer.data)

@api_view(['GET', 'POST'])
def high_score_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = HighScoreSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    obj = HighScore.objects.all()
    serializer = HighScoreSerializer(obj, many=True)

    return Response(serializer.data)

class LibraryAPIView(ModelViewSet):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()

class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

@api_view([HTTPMethod.GET])
def customer_list_API(request):
    queryset = Customer.objects.all()


    # for relative urls  "/usr/2/" == {'request': None}
    # for Absolute urls ==  {'request': request}
    serializer  = CustomerSerializer(queryset, many=True, context={'request': request})

    return Response(serializer.data, HTTPStatus.OK)

class CustomerRetrieveAPI(RetrieveAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'name'



@api_view(['POST', 'GET'])
def author_view(request):
    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)
    
    serializer = AuthorSerializer(Author.objects.all(), many=True)
    return Response(serializer.data, HTTPStatus.CREATED)



class BookAuthorAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializerTwo


class BookCreateAPIView(CreateAPIView):
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class BookCreateAPIView(CreateAPIView):
#     serializer_class = BookSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class MonitorAPIView(ListCreateAPIView):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

class PostAPIViewFour(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializerFour(queryset, many=True)

        return Response(serializer.data, HTTPStatus.OK)
    
    def post(self, request):
        serializer = PostSerializerFour(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data)


class PostListRetrieveAPIViewThree(ListAPIView, RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerThree

class UserRetrieveAPIViewThree(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OwnerSerializerThree

@api_view([HTTPMethod.GET])
def post_list_api_view_two(request):
    queryset = Post.objects.all()
    serializer = PostSerializerTwo(queryset, many=True)

    return Response(serializer.data, HTTPStatus.OK)


class LikeListAPIView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

like_list_api_view = LikeListAPIView.as_view()

class RetrieveLikeAPIView(RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        x = obj.obj_url(self.request)
        return obj

@api_view([HTTPMethod.GET, HTTPMethod.POST])
def index(request, pk=None):
    if request.method == HTTPMethod.POST:
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTPStatus.CREATED)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, HTTPStatus.OK)


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        owner = ...
        if not self.request.user.is_anonymous:
            owner = self.request.user
        else:
            owner = None

        instance = serializer.save(owner=owner)
        return instance
    
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to access this view
def contact_form_view(request):
    serializer = ContactFormSerializer(data=request.data)  # Use request.data here
    serializer.is_valid(raise_exception=True)  # Raise error if validation fails
    serializer.save()

    return Response({'message': f'Thanks {serializer.validated_data["name"].upper()}!'}, status=HTTPStatus.OK)


class UserCreateAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

class UserListAPIView(ListAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
