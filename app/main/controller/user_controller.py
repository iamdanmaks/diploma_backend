from flask import request
from flask_restplus import Resource

from ..util.dtos.user_dto import UserDto
from ..service.user_service import save_new_user, get_a_user, edit_user, delete_user
from ..util.decorator import token_required, organization_admin_token_required


api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @token_required
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
    

    @api.doc('edit a user')
    @token_required
    def put(self, public_id):
        """edit a user given its identifier"""
        data = request.json
        return edit_user(public_id, data)
    
    @api.doc('edit a user')
    @token_required
    def delete(self, public_id):
        """delete a user given its identifier"""
        return delete_user(public_id)
