import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine


# An environment variable for "ENVIRONMENT" must be set to "staging", or "production" for those
# environments. If environment = "staging" or "production", env variables must be established
# in lieu of secrets.json.

# Local configuration settings - relies on secrets.json
if os.path.exists('secrets.json'):
    
    f = open('secrets.json')
    secrets = json.load(f)

    # Authentication Settings
    os.environ['SECRET_KEY'] = secrets['SECRET_KEY']

    # DB Settings
    os.environ['DB_USER'] = secrets['DB_USER']
    os.environ['DB_PASSWORD'] = secrets['DB_PASSWORD']
    os.environ['DB_HOST'] = secrets['DB_HOST']
    os.environ['DB_HOST_PORT'] = secrets['DB_HOST_PORT']
    os.environ['DB_NAME'] = secrets['DB_NAME']

    # Google API Settings
    os.environ['GOOGLE_API_KEY'] = secrets['GOOGLE_API_KEY']


# General configuration settings
class Config(object):

    # Authentication Settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    # DB Settings
    SQLALCHEMY_DATABASE_URI = engine.URL.create(
        'postgresql',
        username=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_HOST_PORT'),
        database=os.environ.get('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google API Settings
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

