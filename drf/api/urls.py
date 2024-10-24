from django.urls import path
from . import cb_views as views
from . import views as regular_views
from . import set_views






urlpatterns = [
    # Start Index

    # path('', regular_views.index, name='products'),
    # path('gt/<str:pk>/', regular_views.index, name='product-details'),
    # path('up/<str:pk>/', regular_views.index, name='update-product'),
    # path('dl/<str:pk>/', regular_views.index, name='delete-product'),

    # End Index


    # Start API View

    # path('', views.CustomAPIView.as_view(), name='products'),
    # path('gt/<int:pk>/', views.CustomAPIView.as_view(), name='product-details'),
    # path('up/<int:pk>/', views.CustomAPIView.as_view(), name='update-product'),
    # path('dl/<int:pk>/', views.CustomAPIView.as_view(), name='delete-product'),

    # Start API View

    # Start Throttle

    # path('throttle/view/', views.throttle_view, name="throttle-view"),
    # path('throttle/view/', views.ThrottleView.as_view(), name="throttle-view"),

    # End Throttle

    # Start Generic Views

    # path('api/upload/', views.image_receiver_view, name='image-receiver-view'),

    # path('products/', views.custom_list_api_view, name='custom_list_api_view'),

    # path('products/<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='product-retrieve'),

    # path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),

    # path('products/update/<int:product_id>/', views.ProductUpdateAPIView.as_view(), name='product-update'),

    # path('products/delete/<str:pk>/', views.ProductDestroyAPIView.as_view(), name='product-delete'),

    # path('products/list/create/', views.ProductListCreateAPIView.as_view(), name='product-create-list'),

    # path('products/retrieve/delete/<str:product_id>/', views.ProductRetrieveDestroyAPIView.as_view(), name='product-delete-get'),
    
    # Start Generic Views

    # Start Mixins Views
    # path('products/mixins/', views.ProductAPIMixinsView.as_view(), name='products-mixins'),

    # path('products/mixins/<int:id>/', views.ProductAPIMixinsView.as_view(), name='products-mixins'),

    # path('products/mixins/retrieve/<str:name>/', views.ProductMixinRetrieveAPIView.as_view()),
    
    # Start Mixins Views


]
