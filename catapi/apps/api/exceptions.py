from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction

from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from catapi.settings import REST_FRAMEWORK


class PayloadTooLarge(exceptions.APIException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = 'Payload size is too large.'
    default_code = 'size_limit_exceeded'


def set_rollback():
    atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)


def core_exception_handler(exc, context):
    """ Mostly repeats rest_framework.views.exception_handler, but the error
    message is assembled in different uniform way, for easier parsing in front
    end app.
    1. Error code is in the status
    2. 'errors' is always a list of one or more errors
    3. Each error is a dict with 'type'(e.g. 'ValidationError', 'NotFound' etc)
       and 'message' with error particulars.
    """
    exception_data = {
        'errors': []
    }
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        if isinstance(exc.detail, list):
            for element in exc.detail:
                exception_data['errors'].append({'message': element.detail})
        elif isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if key == REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']:
                    prefix = ''
                else:
                    prefix = '[{}] '.format(key)
                exception_data['errors'].append({
                    'type': exc.__class__.__name__,
                    'message': '{}{}'.format(prefix, value[0])
                })
        else:
            exception_data['errors'].append({
                'type': exc.__class__.__name__,
                'message': str(exc.detail)
            })
        set_rollback()
        return Response(exception_data, status=exc.status_code, headers=headers)

    return None
