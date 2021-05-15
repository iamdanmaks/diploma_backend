from flask_restplus import Namespace, fields


class QueryDto:
    api = Namespace('query', description='query related operations')
    query = api.model('query', {
        'text': fields.String(description='text to voice'),
        'voice': fields.String(description='voice public id'),
        'organization': fields.String(description='organization public id')
    })
