from rest_framework.exceptions import APIException

class CustomValidatorNameException(APIException):
    status_code = 400
    default_detail = {'name': "this field is required"}
    default_code = 'Invalid name'