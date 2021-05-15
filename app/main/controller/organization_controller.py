from flask import request
from flask_restplus import Resource

from ..util.dtos.organization_dto import OrganizationDto
from ..service.organization_service import get_organization, edit_organization, delete_organization
from ..service.organization_service import change_api_key, get_api_key
from ..service.organization_service import add_organization_admin, remove_organization_member
from ..util.decorator import token_required, organization_admin_token_required


api = OrganizationDto.api
_organization = OrganizationDto.organization


@api.route('/')
@api.response(404, 'Organization not found.')
class Organization(Resource):
    @api.doc('get an organization')
    @token_required
    def get(self):
        """get organization given its identifier"""
        organization = get_organization(request.headers.get('Authorization'))
        if not organization:
            api.abort(404)
        else:
            return organization
    

    @api.doc('edit organization')
    @organization_admin_token_required
    def put(self):
        """edit organization given its identifier"""
        data = request.json
        return edit_organization(request.headers.get('Authorization'), data)


    @api.doc('delete organization')
    @organization_admin_token_required
    def delete(self):
        """delete organization given its identifier"""
        return delete_organization(request.headers.get('Authorization'))


@api.route('/key')
@api.response(404, 'Organization not found.')
class OrganizationApiKey(Resource):
    @api.doc('get an organization api key')
    @token_required
    def get(self):
        """get organization given its identifier"""
        organization_key = get_api_key(request.headers.get('Authorization'))
        if not organization_key:
            api.abort(404)
        else:
            return organization_key
    

    @api.doc('edit organization')
    @organization_admin_token_required
    def put(self):
        """edit organization given its identifier"""
        return change_api_key(request.headers.get('Authorization'))


@api.route('/members/access/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class OrganizationMembers(Resource):
    @api.doc('add organization admin')
    @organization_admin_token_required
    def post(self, public_id):
        """add admin given user identifier"""
        return add_organization_admin(public_id)

    
    @api.doc('remove organization member')
    @organization_admin_token_required
    def delete(self, public_id):
        """delete a member given user identifier"""
        return remove_organization_member(request.headers.get('Authorization'), public_id)
