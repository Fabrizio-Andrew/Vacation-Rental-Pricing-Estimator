from routes import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON


class User(UserMixin, db.Model):
    """User of the site."""

    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def get_id(self):
        return self.uid