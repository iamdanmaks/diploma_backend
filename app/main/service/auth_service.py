from app.main.model.user import User
from app.main.model.organization import Organization
from ..service.token_service import encode_auth_token, decode_auth_token
from ..service.blacklist_service import save_token
from flask_babel import _


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email_username')).first()

            if not user:
                user = User.query.filter_by(username=data.get('email_username')).first()

            if user and user.check_password(data.get('password')):
                auth_token = encode_auth_token(days=1, seconds=5, user_id=user.public_id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': _('Successfully logged in.'),
                        'Authorization': auth_token
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': _('email or password does not match.')
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': _('Try again')
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not resp.startswith('ERROR:'):
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': _('Provide a valid auth token.')
            }
            return response_object, 403
    
    @staticmethod
    def get_logged_in_entity(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp, token_type = decode_auth_token(auth_token)
            if not resp.startswith('ERROR:'):
                if token_type == 'USR':
                    entity = User.query.filter_by(public_id=resp).first()
                    
                    if not entity:
                        return {
                            'status': 'fail',
                            'message': _('User not found')
                        }, 404
                    
                    response_object = {
                        'status': 'success',
                        'data': {
                            'type': 'USR',
                            'id': entity.id,
                            'public_id': entity.public_id,
                            'email': entity.email,
                            'admin': entity.admin,
                            'registered_on': str(entity.registration_date),
                            'email_confirmed': entity.email_confirmed,
                            'organization_confirmed': entity.organization_confirmed,
                            'organization_admin': entity.organization_admin
                        }
                    }

                else:
                    entity = Organization.query.filter_by(public_id=resp).first()

                    if not entity:
                        return {
                            'status': 'fail',
                            'message': _('Organization not found')
                        }, 404

                    response_object = {
                        'status': 'success',
                        'data': {
                            'type': 'ORG',
                            'id': entity.id,
                            'public_id': entity.public_id,
                            'registered_on': str(entity.registration_date),
                            'is_demo': entity.is_demo,
                            'tokens_left': entity.demo_tokens_left
                        }
                    }
                
                return response_object, 200
            
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': _('Provide a valid auth token.')
            }
            return response_object, 401
