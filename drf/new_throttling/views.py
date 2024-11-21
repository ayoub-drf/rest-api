from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    ScopedRateThrottle,
    BaseThrottle,

)
from rest_framework.decorators import (
    api_view,
    throttle_classes
)

from django.core.cache import cache


class CustomBaseThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip_address = request.META.get("REMOTE_ADDR")
        key = f"ip_{ip_address}"
        request_count = cache.get(key=key, default=0)

        if request_count < 5:
            cache.set(key=key, value=request_count + 1, timeout=30)
            return True
        
        return False


    def wait(self): # Be aware of caching expiration time (the wait function must wait till the cache be empty)
        return 30
    

class CustomAnonRateThrottle(AnonRateThrottle):
    rate = "5/day"

class CustomAnonUserRateThrottle(UserRateThrottle):
    rate = "10/day"

from .throttling import BurstRateThrottle

@api_view(['GET'])
@throttle_classes([BurstRateThrottle])
def register(request):

    return Response({"msg": "Hello world"})

class Register(APIView):
    # throttle_classes = [CustomBaseThrottle] # 5 request per half minute

    # throttle_scope = 'special_scope_two'  # use the special_scope_two for this view

    # throttle_scope = 'default'  # use the default for this view

    # throttle_classes = [] # No Throttling for this view

    # throttle_classes = [AnonRateThrottle] # Use Anonymous throttling for this view
    # throttle_classes = [AnonRateThrottle, UserRateThrottle] # Use Anonymous & User throttling for this view

    def get(self, request):
        return Response({"message": "ok"})