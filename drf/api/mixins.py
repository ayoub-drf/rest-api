from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

class MultipleLookUPFiledMixin:
    permission_classes = [IsAdminUser]
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}

        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter[field] = self.kwargs.get(field)

        obj = get_object_or_404(queryset, **filter)
        # self.check_permissions(self.request, obj)

        return obj
