from .. import db, flask_bcrypt


class Voice(db.Model):
    """ Voice Model for storing voice related details """
    __tablename__ = "voice"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    
    is_general = db.Column(db.Boolean, nullable=False, default=False)

    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    query_id = db.relationship("Query")
    

    def __repr__(self):
        return "<Voice '{}'>".format(self.name)
