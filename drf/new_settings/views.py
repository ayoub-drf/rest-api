from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.settings import api_settings


class SimpleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        print(dir(api_settings))
        
        print("-" * 100)
        print('ALLOWED_VERSIONS : ', api_settings.ALLOWED_VERSIONS)

        print("-" * 100)
        print('COMPACT_JSON : ', api_settings.COMPACT_JSON)

        print("-" * 100)
        print('DEFAULT_AUTHENTICATION_CLASSES : ', api_settings.DEFAULT_AUTHENTICATION_CLASSES)

        print("-" * 100)
        print('DEFAULT_CONTENT_NEGOTIATION_CLASS : ', api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS)

        print("-" * 100)
        print('DEFAULT_METADATA_CLASS : ', api_settings.DEFAULT_METADATA_CLASS)

        print("-" * 100)
        print('DEFAULT_PARSER_CLASSES : ', api_settings.DEFAULT_PARSER_CLASSES)

        print("-" * 100)
        print('DEFAULT_PERMISSION_CLASSES : ', api_settings.DEFAULT_PERMISSION_CLASSES)

        print("-" * 100)
        print('DEFAULT_RENDERER_CLASSES : ', api_settings.DEFAULT_RENDERER_CLASSES)

        print("-" * 100)
        print('DEFAULT_VERSION : ', api_settings.DEFAULT_VERSION)

        print("-" * 100)
        print('DEFAULT_VERSIONING_CLASS : ', api_settings.DEFAULT_VERSIONING_CLASS)

        print("-" * 100)
        print('FORMAT_SUFFIX_KWARG : ', api_settings.FORMAT_SUFFIX_KWARG)

        print("-" * 100)
        print('PAGE_SIZE : ', api_settings.PAGE_SIZE)

        print("-" * 100)
        print('STRICT_JSON : ', api_settings.STRICT_JSON)

        print("-" * 100)
        print('UNICODE_JSON : ', api_settings.UNICODE_JSON)

        print("-" * 100)
        print('URL_FORMAT_OVERRIDE : ', api_settings.URL_FORMAT_OVERRIDE)

        print("-" * 100)
        print('VERSION_PARAM : ', api_settings.VERSION_PARAM)
        return Response()
