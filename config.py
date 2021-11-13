import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine


# An environment variable for "ENVIRONMENT" must be set to "staging", or "production" for those
# environments. If environment = "staging" or "production", env variables must be established
# in lieu of secrets.json.

# Local configuration settings - relies on docker compose & secrets.json
if os.environ.get('APP_SETTINGS') == 'DevelopmentConfig':
    
    f = open('secrets.json')
    secrets = json.load(f)

    # Authentication Settings
    os.environ['AUTH0_CLIENT_ID'] = secrets['AUTH0_CLIENT_ID']
    os.environ['AUTH0_CLIENT_SECRET'] = secrets['AUTH0_CLIENT_SECRET']
    os.environ['APP_URL'] = 'http://localhost:5000'
    os.environ['AUTH0_CALLBACK_URL'] = 'http://localhost:5000/callback'

    # DB Settings
    os.environ['DB_USER'] = secrets['DB_USER']
    os.environ['DB_PASSWORD'] = secrets['DB_PASSWORD']
    os.environ['DB_HOST'] = secrets['DB_HOST']
    os.environ['DB_HOST_PORT'] = secrets['DB_HOST_PORT']
    os.environ['DB_NAME'] = secrets['DB_NAME']


# General configuration settings
class Config(object):

    # Authentication Settings
    API_BASE_URL = 'https://dev-l0m79glj.us.auth0.com'
    AUTH0_ACCESS_TOKEN_URL = API_BASE_URL + '/oauth/token'
    AUTH0_AUTHORIZE_URL = API_BASE_URL + '/authorize'
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_CLIENT_KWARGS = {
        'scope': 'openid profile email'
    }
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    # DB Settings
    SQL_URL = engine.URL.create(
        'postgresql',
        username=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_HOST_PORT'),
        database=os.environ.get('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Local configuration settings - relies on docker compose
class DevelopmentConfig(Config):

    # Authentication Settings
    APP_URL = 'http://localhost:5000'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'


# Staging configuration settings - relies on Heroku env variables
class StagingConfig(Config):

    # Authentication Settings
    APP_URL = 'https://immense-mountain-68865.herokuapp.com'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'



# Production configuration settings - relies on Heroku env variables
class ProductionConfig(Config):

    # Authentication Settings
    APP_URL = 'https://vacation-rental-estimator-prod.herokuapp.com'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'

