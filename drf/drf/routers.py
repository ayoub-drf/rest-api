# from rest_framework.routers import DefaultRouter, SimpleRouter

# from api.viewsets import UserViewSet



# router = DefaultRouter(trailing_slash=False) # http://127.0.0.1:8000/api/users
# router = DefaultRouter(trailing_slash=True) # http://127.0.0.1:8000/api/users/ 
# router.register(prefix='products', viewset=ProductListRetrieveViewSet, basename='product')
# router.register(prefix=r'users', viewset=UserViewSetGenericViewSet, basename='user')
# router.register(prefix=r'users', viewset=UserViewSet, basename='user')
# router.register('products', ProductListRetrieveViewSet, basename='product')
# router.register(prefix=r'users', viewset=UserList, basename='user')


# from api.custom_routers import CustomReadOnlyRouter

# router = CustomReadOnlyRouter(trailing_slash=True)
# router.register('users', UserViewSet)

# from core.views import LibraryAPIView

# from api.renders import AdminRendererAPIView
# router = DefaultRouter()
# router.register(prefix='^products', viewset=AdminRendererAPIView, basename='product')

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(prefix=r'child', viewset=ChildModelViewSet, basename='child')

# urlpatterns = router.urls