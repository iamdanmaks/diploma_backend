from .. import db, flask_bcrypt
import datetime
from langdetect import detect


class Query(db.Model):
    """ Query Model for storing query related details """
    __tablename__ = "query"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)

    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)
    
    lang = db.Column(db.String(5))
    time_processed = db.Column(db.Integer)

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    voice_id = db.Column(db.Integer, db.ForeignKey('voice.id'), nullable=True)
    

    def __init__(self, public_id, text):
        self.public_id = public_id
        self.text = text
        self.token_num = len(text)
        self.lang = detect(text)
        self.date = datetime.datetime.now()
