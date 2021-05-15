import boto3
from botocore.client import Config

from flask import Flask
from flask import request
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_babel import Babel

from .admin.custom_view import *
from .config import Config as cnfg, config_by_name


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()
cors = CORS(resources={r"/api/*": {"origins": "*"}})
babel = Babel()
admin = Admin(name='EasyVoice', template_mode='bootstrap4')

client = boto3.client(
        's3',
        aws_access_key_id=cnfg.AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=cnfg.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2',
        config=Config(signature_version='s3v4')
    )


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'uk'])


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    babel.init_app(app)
    admin.init_app(app)

    from app.main.model import User, Voice, UnsignedQuery, BlacklistToken, Organization, Query

    admin.add_view(UserView(User, db.session))
    admin.add_view(OrganizationView(Organization, db.session))
    admin.add_view(VoiceView(Voice, db.session))
    admin.add_view(UnsignedQueryView(UnsignedQuery, db.session))
    admin.add_view(QueryView(Query, db.session))
    admin.add_view(CustomModelView(BlacklistToken, db.session))

    from app.main.admin.backup import BackupView

    admin.add_view(BackupView(name='Backup', endpoint='backup'))

    return app
