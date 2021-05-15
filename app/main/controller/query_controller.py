from flask import request
from flask_restplus import Resource

from ..util.dtos.query_dto import QueryDto
from ..service.query_service import get_queries, signed_voicing_query, unsigned_voicing_query
from ..util.decorator import token_required, organization_admin_token_required, organization_token_required


api = QueryDto.api
_query = QueryDto.query


@api.route('/')
class QueryList(Resource):
    @api.response(200, 'Query successfully processed.')
    @api.doc('process query')
    @api.expect(_query)
    @organization_token_required
    def post(self):
        """Process new query """
        data = request.json
        return signed_voicing_query(data)
    
    @api.doc('get queries')
    @organization_token_required
    def get(self):
        """get a voice list"""
        return get_queries(request.args.get('organization'))


@api.route('/demo')
class QueryUnsigned(Resource):
    @api.response(200, 'Unsigned query was processed.')
    @api.doc('voice text demo')
    def post(self):
        return unsigned_voicing_query(request.remote_addr, request.json)
