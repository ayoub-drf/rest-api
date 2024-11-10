from django.urls import path, include
from .views import (
    index,
    PostListCreateAPIView,
    contact_form_view,
    like_list_api_view,
    RetrieveLikeAPIView,
    UserCreateAPIView,
    UserListAPIView,
    post_list_api_view_two,
    PostListRetrieveAPIViewThree,
    UserRetrieveAPIViewThree,
    PostAPIViewFour,
    MonitorAPIView,
    BookCreateAPIView,
    BookAuthorAPIView,
    author_view,
    customer_list_API,
    CustomerRetrieveAPI,
    ProductDetailAPIView,
    LibraryAPIView,
    high_score_view,
    name_view,
    user_api_view_ten,
)



urlpatterns = [
    path('users/', user_api_view_ten),
    path('name/', name_view),


    # path('', index),
    # path('post/', PostListCreateAPIView.as_view()),
    # path('contact/', contact_form_view),

    # path('', like_list_api_view),
    # path('retr/<int:pk>/', RetrieveLikeAPIView.as_view(), name='retrieve-like'),
    # path('create-user/', UserCreateAPIView.as_view()),
    # path('list-user/', UserListAPIView.as_view()),

    # path('post-list/', post_list_api_view_two),

    path('', PostListRetrieveAPIViewThree.as_view()),
    path('get/<int:pk>/', PostListRetrieveAPIViewThree.as_view(), name='post-detail'),
    path('usr/<int:pk>/', UserRetrieveAPIViewThree.as_view(), name='user-detail'),

    path('posts/', PostAPIViewFour.as_view()),

    path('monitors/', MonitorAPIView.as_view()),

    path('create-book/', BookCreateAPIView.as_view()),

    path('book-author/', BookAuthorAPIView.as_view()),

    path('create-author/', author_view),

    path('customers/',customer_list_API, name='customers'),

    path('customers/<str:name>/', CustomerRetrieveAPI.as_view(), name='customers-detail'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='products-detail'),



]
