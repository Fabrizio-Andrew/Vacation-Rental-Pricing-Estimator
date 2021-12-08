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

class Property(db.Model):
    """Properties owned by users."""

    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(512), nullable=False)
    HostResponseTime = db.Column(db.Integer, nullable=False)
    RoomType = db.Column(db.Integer, nullable=False)
    Beds = db.Column(db.Integer, nullable=False)
    Accommodates = db.Column(db.Integer, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    ReviewScore = db.Column(db.Float, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable = False)