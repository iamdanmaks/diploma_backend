from .token_service import encode_auth_token, decode_auth_token
from app.main import db

from flask_babel import _

from app.main.service.user_service import map_user

from app.main.model.user import User
from app.main.model.organization import Organization
from app.main.model.voice import Voice
from app.main.model.query import Query


def find_organization_by_token(token):
    user_public_id, token_type = decode_auth_token(token)
    user = User.query.filter_by(public_id=user_public_id).first()

    return Organization.query.filter_by(id=user.organization_id).first()


def get_organization(token):
    organization = find_organization_by_token(token)
    
    if not organization:
        return {
            'status': 'fail',
            'message': _('Organization not found')
        }, 404
    
    users = [map_user(u) for u in organization.user_id if u.email_confirmed and u.organization_confirmed]

    return {
        'public_id': organization.public_id,
        'name': organization.name,
        'description': organization.description,
        'api_key': organization.api_token,
        'registration_date': str(organization.registration_date),
        'demo': organization.is_demo,
        'tokens_left': organization.demo_tokens_left,
        'users': users
    }


def edit_organization(token, data):
    organization = find_organization_by_token(token)

    if organization:
        if 'description' in data:
            organization.description = data.get('description')
        if 'card_token' in data:
            organization.card_token = data.get('card_token')
        if 'demo_status' in data:
            organization.is_demo = data.get('demo_status')
        
        db.session.commit()
        return {
            'status': 'success',
            'message': _('Organization was successfully edited')
        }, 200

    else:
        return {
            'status': 'fail',
            'message': _('Organization not found')
        }, 404


def delete_organization(token):
    try:
        organization = find_organization_by_token(token)

        for u in organization.user_id:
            User.query.filter_by(id=u.id).delete()

        for v in organization.voice_id:
            Voice.query.filter_by(id=v.id).delete()
        
        for q in organization.query_id:
            Query.query.filter_by(id=q.id).delete()

        Organization.query.filter_by(id=organization.id).delete()
        db.session.commit()
    except Exception as e:
        print(e)
        return {
            'status': 'fail',
            'message': _('Something went wrong')
        }, 400

    return {
        'status': 'success',
        'message': _('Organization was successfully deleted')
    }, 200


def get_api_key(token):
    organization = find_organization_by_token(token)
    
    if not organization:
        return {
            'status': 'fail',
            'message': _('Organization is not found')
        }, 404
    
    token = organization.api_token
    
    return {
        'status': 'success',
        'message': _('Key is found'),
        'token': token
    }, 200


def change_api_key(token):
    organization = find_organization_by_token(token)
    
    if not organization:
        return {
            'status': 'fail',
            'message': _('Organization is not found')
        }, 404

    token = encode_auth_token(
                days=365*1000, 
                seconds=5, 
                organization_id=organization.public_id
            )
    
    organization.api_token = token
    db.session.commit()
    
    return {
        'status': 'success',
        'message': _('Key is changed'),
        'token': token
    }, 200


def add_organization_admin(usr_public_id):
    user = User.query.filter_by(public_id=usr_public_id).first()
    
    if not user:
        return {
            'status': 'fail',
            'message': _('User not found')
        }, 404
    
    user.organization_admin = not user.organization_admin
    db.session.commit()

    return {
        'status': 'success',
        'message': _('Organization admin access was changed')
    }, 200


def remove_organization_member(token, usr_public_id):
    try:
        organization = find_organization_by_token(token)
        user = User.query.filter_by(public_id=usr_public_id).first()

        organization.user_id.remove(user)

        User.query.filter_by(public_id=usr_public_id).delete()

        db.session.commit()
    except Exception as e:
        print(e)
        return {
            'status': 'fail',
            'message': _('Something went wrong')
        }, 400

    return {
        'status': 'success',
        'message': _('Organization member was successfully deleted')
    }, 200
