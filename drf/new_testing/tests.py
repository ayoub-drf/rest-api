from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
)
from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)
import json
from django.contrib.auth.models import User
from .views import PostAPIView


factory = APIRequestFactory()




# req = factory.get('/posts/', format="json")
# view = PostAPIView.as_view()
# res = view(req)
# print(res.data)
# assert res.status_code == 200


# data = {'name': 'Post 111', 'author': 1}
# req = factory.post(
#     '/posts/',
#     data=json.dumps(data),
#     content_type='application/json' 
# )
# view = PostAPIView.as_view()
# res = view(req)

# assert res.status_code == 201

class ProtectedViewTestCase(TestCase):
    def test_authenticated_access(self):
        user = User.objects.create_superuser(username="x", password="x")

        request = factory.get('/posts/')

        force_authenticate(request, user=user)

        view = PostAPIView.as_view()
        response = view(request)

        assert response.status_code == 200  # OK
