from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
    NotAuthenticated,
    PermissionDenied
)

from .serializers import PostSerializer
from .models import Post

class PostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated("Login required", HTTP_403_FORBIDDEN)
        
        if not request.user.is_staff:
            raise PermissionDenied("you dont have the permmissions", HTTP_401_UNAUTHORIZED)
        
        pk = kwargs.get('pk')

        if pk is not None:
            try:
                post = Post.objects.get(pk=pk)
                print(request.data)
                serializer = PostSerializer(post)
                return Response(serializer.data, HTTP_200_OK)
            except Post.DoesNotExist:
                raise NotFound(f'post with this is ({pk}) does not exists', HTTP_404_NOT_FOUND)
            
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, HTTP_201_CREATED)

    


