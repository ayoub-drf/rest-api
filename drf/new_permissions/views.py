from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied


from django.shortcuts import get_object_or_404

from .models import (
    Person
)
from .serializers import (
    PersonSerializer
)



# console.log@@


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    
class IsAuthenticatedPermissionAndStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class PersonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


    def get_queryset(self):
        print(self.request.META['REMOTE_ADDR'])

        return Person.objects.filter(owner=self.request.user)

    # def get_object(self):
    #     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, obj)

    #     if obj.owner != self.request.user:
    #         raise PermissionDenied("You do not have permission to access this object.")

    #     return obj





