from flask_restplus import Namespace, fields


class OrganizationDto:
    api = Namespace('organization', description='organization related operations')
    organization = api.model('organization', {
        'description': fields.String(description='organization name'),
        'card_token': fields.String(description='organization card token'),
        'demo_status': fields.Boolean(description='organization demo status'),
    })
