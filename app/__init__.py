from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.organization_controller import api as organization_ns
from .main.controller.voice_controller import api as voice_ns
from .main.controller.query_controller import api as query_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
            title='FLASK VOICE-OVER',
            version='1.0',
            description='flask restplus web service'
          )

api.add_namespace(user_ns, path='/api/user')
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(organization_ns, path='/api/organization')
api.add_namespace(voice_ns, path='/api/voice')
api.add_namespace(query_ns, path='/api/query')
