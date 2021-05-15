import datetime
import jwt
from ..model.blacklist_token import BlacklistToken
from ..model.organization import Organization
from ..config import key


def encode_auth_token(days, seconds, user_id=None, organization_id=None):
    try:
        if user_id:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'type': 'USR',
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        elif organization_id:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'type': 'ORG',
                'sub': organization_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token.split(' ')[1], key, algorithms=['HS256'])
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'ERROR: Token blacklisted. Please log in again.', None
        else:
            return payload['sub'], payload['type']
    except jwt.ExpiredSignatureError:
        return 'ERROR: Signature expired. Please log in again.', None
    except jwt.InvalidTokenError:
        return 'ERROR: Invalid token. Please log in again.', None
