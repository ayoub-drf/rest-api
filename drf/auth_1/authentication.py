from rest_framework.authentication import TokenAuthentication

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        if not api_key:
            raise AuthenticationFailed('authentication required')

        try:
            api_key = ApiKey.objects.get(api_key=api_key)
            user = api_key.user
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

        return (user, api_key)

class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"