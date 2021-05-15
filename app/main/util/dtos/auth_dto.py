from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email_username': fields.String(required=True, description='The email address or username'),
        'password': fields.String(required=True, description='The user password '),
    })
