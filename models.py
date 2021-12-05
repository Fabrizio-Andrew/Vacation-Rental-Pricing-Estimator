from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    email_verified = db.Column(db.Boolean)
    family_name = db.Column(db.String(40))
    given_name = db.Column(db.String(40))
    locale = db.Column(db.String())
    name = db.Column(db.String(80))
    nickname = db.Column(db.String(80))
    picture = db.Column(db.String())
    sub = db.Column(db.String())
    updated_at = db.Column(db.String())
    last_login = db.Column(db.DateTime)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)