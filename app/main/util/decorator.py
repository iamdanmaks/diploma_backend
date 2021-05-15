from flask_babel import _

from functools import wraps
from flask import request

from app.main.service.auth_service import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_entity(request)
        token = data.get('data')

        if not token:
            return data, status

        if token['type'] == 'ORG':
            response_object = {
                'status': 'fail',
                'message': _('This operations should be done from user account')
            }
            return response_object, 401
        
        if not token['email_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Confirm your email')
            }
            return response_object, 401

        if not token['organization_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Your organization is still not confirmed')
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def organization_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_entity(request)
        token = data.get('data')

        if not token:
            return data, status

        if token['type'] == 'USR' and not token['email_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Confirm your email')
            }
            return response_object, 401

        if token['type'] == 'USR' and not token['organization_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Your organization is still not confirmed')
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def organization_admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_entity(request)
        token = data.get('data')

        if not token:
            return data, status
        
        if token['type'] == 'ORG':
            response_object = {
                'status': 'fail',
                'message': _('This operations should be done from user account')
            }
            return response_object, 401

        if not token['email_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Confirm your email')
            }
            return response_object, 401

        if not token['organization_confirmed']:
            response_object = {
                'status': 'fail',
                'message': _('Your organization is still not confirmed')
            }
            return response_object, 401
        
        if not token['organization_admin']:
            response_object = {
                'status': 'fail',
                'message': _('You are not organization admin')
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_entity(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': _('admin token required')
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
