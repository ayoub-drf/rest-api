from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('api.urls')),

    # path('api/', include(('drf.routers', 'my_routers')))

    path('api/', include('drf.routers')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from .routers import router
# urlpatterns += router.urls
