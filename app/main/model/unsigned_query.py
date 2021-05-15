from .. import db, flask_bcrypt


class UnsignedQuery(db.Model):
    """ Unsigned Query Model for storing unsgined query limit details """
    __tablename__ = "unsigned_query"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(255), unique=True, nullable=False)
    
    tokens_left = db.Column(db.Integer, nullable=False, default=1000)
    last_query = db.Column(db.DateTime)

    def __repr__(self):
        return "<IP address '{}'>".format(self.ip_address)
