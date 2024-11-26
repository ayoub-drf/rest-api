from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Book API",
      default_version='v1',
      description="This is a Book API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@bookapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('docs/', schema_view.as_view(), name='docs'),

    path('admin/', admin.site.urls),

    # path('', include('api.urls')),
    
    # path('', include('books.urls')),
    # path('', include('core.urls')),

    # path('c/', include(('drf.routers', 'my_routers'))),

    path('', include('new_schemas.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from .routers import router
# urlpatterns += router.urls
