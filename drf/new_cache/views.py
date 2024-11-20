from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import (
    vary_on_cookie,
    vary_on_headers
)
from django.http import HttpResponse
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response

def my_decorator(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        print(dir(response))
        return response
    return wrapper

@api_view(['GET'])
@cache_page(60 * 60)
@vary_on_headers("User-Agent")
def api(request):
    print('Start caching')
    time.sleep(10)
    serializer = {
        "msg": "hello"
    }

    return Response(serializer)


# class UserViewSet:
#     @method_decorator(cache_page(60 * 60 * 2))
#     @method_decorator(vary_on_cookie)
    
# @vary_on_cookie
# @cache_page(60 * 60) 
# def index(request, val=None):
#     time.sleep(4)
#     response = HttpResponse(f"The current language is {val}.")
#     if val:
#         response.set_cookie('language', val)

#     return response
    
class MyView(View):
    @method_decorator(cache_page(60 * 60))

    
    def get(self, request):
        time.sleep(10)
        return HttpResponse('Hello world')