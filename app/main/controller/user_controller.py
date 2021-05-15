from flask import request
from flask_restplus import Resource

from ..util.dtos.user_dto import UserDto
from ..service.user_service import save_new_user, get_a_user, edit_user, delete_user
from ..service.user_service import confirm_email, invite_user, reset_password, reset_link
from ..util.decorator import token_required, organization_admin_token_required


api = UserDto.api
_user = UserDto.user


@api.route('/')
class User(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)
    
    @api.doc('get a user')
    @token_required
    def get(self):
        """get a user given its identifier"""
        user = get_a_user(request.headers.get('Authorization'))
        if not user:
            api.abort(404)
        else:
            return user
    

    @api.doc('edit a user')
    @token_required
    def put(self):
        """edit a user given its identifier"""
        data = request.json
        return edit_user(request.headers.get('Authorization'), data)
    
    
    @api.doc('edit a user')
    @token_required
    def delete(self):
        """delete a user given its identifier"""
        return delete_user(request.headers.get('Authorization'))


@api.route('/confirm')
class UserConfirm(Resource):
    @api.response(200, 'User email successfully confirmed.')
    @api.doc('confirm a new user')
    def get(self):
        """Confirm a new user """
        data = request.args.get('token')
        return confirm_email(data)


@api.route('/invite')
class UserInvite(Resource):
    @api.response(200, 'User successfully invited.')
    @api.doc('invite a new user')
    def post(self):
        """Invite a new user """
        return invite_user(request.headers.get('Authorization'), request.json.get('email'))


@api.route('/reset-password')
class UserReset(Resource):
    @api.response(200, 'User successfully reseted password.')
    @api.doc('reset a password')
    def put(self):
        """Reset a password """
        data = request.json
        return reset_password(
            data.get('token'),
            data.get('password')
        )
    
    @api.response(200, 'User got emailed.')
    @api.doc('reset a password link')
    def get(self):
        """Reset password link """
        return reset_link(request.args.get('email'))
