import datetime
from .. import db, flask_bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    public_id = db.Column(db.String(100), unique=True)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    
    password_hash = db.Column(db.String(150))

    apply_reason = db.Column(db.String(500))
    registration_date = db.Column(db.DateTime)

    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    organization_confirmed = db.Column(db.Boolean, nullable=False, default=True)
    organization_admin = db.Column(db.Boolean, nullable=False, default=False)

    admin = db.Column(db.Boolean, nullable=False, default=False)

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
