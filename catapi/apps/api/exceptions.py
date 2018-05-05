from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    detail = response.data.pop('detail', None)
    if detail:
        error_code = exc.get_codes()
        response.data[error_code] = detail
    return _wrap_error_response(response)


def _wrap_error_response(response):
    response.data = {
        'status': 'error',
        'message': response.data
    }
    return response


class PayloadTooLarge(APIException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = 'Payload size is too large.'
    default_code = 'size_limit_exceeded'
