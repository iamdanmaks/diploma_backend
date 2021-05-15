from flask_restplus import Namespace, fields


class VoiceDto:
    api = Namespace('voice', description='voice related operations')
    voice = api.model('voice', {
        'name': fields.String(description='voice name'),
        'description': fields.String(description='voice description'),
        'organization': fields.String(description='organization public id')
    })
