from api.set_views import ProductListRetrieveViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(prefix='products', viewset=ProductListRetrieveViewSet, basename='product')
router.register(prefix=r'users', viewset=UserViewSet, basename='product')
urlpatterns = router.urls