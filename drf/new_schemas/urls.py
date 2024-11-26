from django.urls import path
from rest_framework.schemas import get_schema_view


from .views import *

urlpatterns = [
    path(
        "openapi",
        get_schema_view(
            title="Your Project", description="API for all things …", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    
]
