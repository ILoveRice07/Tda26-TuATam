import uuid
import datetime
from flask_login import UserMixin
from extensions import db

class Course(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_summary_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "createdAt": self.createdAt.isoformat() + 'Z',
            "updatedAt": self.updatedAt.isoformat() + 'Z'
        }

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = "lecturer"
    
    def get_id(self):
        return str(self.id)
