from flask import request
from flask_restplus import Resource

from ..util.dtos.voice_dto import VoiceDto
from ..service.voice_service import add_voice, edit_voice, remove_voice
from ..service.voice_service import get_voice, get_voices_list, get_general_voice_list
from ..util.decorator import token_required, organization_admin_token_required, organization_token_required


api = VoiceDto.api
_voice = VoiceDto.voice


@api.route('/')
class VoiceList(Resource):
    @api.response(201, 'Voice successfully created.')
    @api.doc('save a new voice')
    @api.expect(_voice)
    @token_required
    def post(self):
        """Creates a new Voice """
        data = request.json
        return add_voice(data, data.get('file'))
    
    @api.doc('get voices')
    @organization_token_required
    def get(self):
        """get a voice list"""
        return get_voices_list(request.args.get('organization'))


@api.route('/<public_id>')
class Voice(Resource):
    @api.response(200, 'Voice data was sent to user.')
    @api.doc('get voice')
    @organization_token_required
    def get(self, public_id):
        return get_voice(public_id)
    
    @api.response(200, 'Voice data was edited.')
    @api.doc('edit voice')
    @token_required
    def put(self, public_id):
        return edit_voice(public_id, request.json)

    @api.response(200, 'Voice was deleted.')
    @api.doc('delete voice')
    @token_required
    def delete(self, public_id):
        return remove_voice(public_id)


@api.route('/general')
class VoiceGeneral(Resource):
    @api.response(200, 'Public voices were sent to user.')
    @api.doc('get general voices')
    def get(self):
        return get_general_voice_list()
