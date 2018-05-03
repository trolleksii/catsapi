from rest_framework.views import exception_handler


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
