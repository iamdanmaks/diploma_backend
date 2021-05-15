from .. import db, flask_bcrypt


class Organization(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    card_token = db.Column(db.String(255))

    api_token = db.Column(db.String(500))

    registration_date = db.Column(db.DateTime)

    is_demo = db.Column(db.Boolean, nullable=False, default=True)
    demo_tokens_left = db.Column(db.Integer, nullable=False, default=300000)

    user_id = db.relationship('User')
    voice_id = db.relationship("Voice")
    query_id = db.relationship("Query")

    def __repr__(self):
        return "<Organization '{}'>".format(self.name)
