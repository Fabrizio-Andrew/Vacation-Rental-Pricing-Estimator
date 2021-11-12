import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import engine


# An environment variable for "ENVIRONMENT" must be set to "staging", or "production" for those
# environments. If environment = "staging" or "production", env variables for AUTH0_CLIENT_ID 
# & AUTH0C_CLIENT_SECRET are also required.

# General configuration settings
class Config(object):
    API_BASE_URL = 'https://dev-l0m79glj.us.auth0.com'
    AUTH0_ACCESS_TOKEN_URL = API_BASE_URL + '/oauth/token'
    AUTH0_AUTHORIZE_URL = API_BASE_URL + '/authorize'
    AUTH0_CLIENT_KWARGS = {
        'scope': 'openid profile email'
    }

    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Local configuration settings - relies on docker compose
class DevelopmentConfig(Config):
    f = open('secrets.json')
    secrets = json.load(f)
    
    # Authentication Settings
    AUTH0_CLIENT_ID = secrets['AUTH0_CLIENT_ID']
    AUTH0_CLIENT_SECRET = secrets['AUTH0_CLIENT_SECRET']
    APP_URL = 'http://localhost:5000'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'

    # DB Settings
    SQL_URL = engine.URL.create(
        'postgresql',
        username=secrets['DB_USER'],
        password=secrets['DB_PASSWORD'],
        host=secrets['DB_HOST'],
        port=secrets['DB_HOST_PORT'],
        database=secrets['DB_NAME']
    )



# Staging configuration settings - relies on Heroku env variables
class StagingConfig(Config):
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    APP_URL = 'https://immense-mountain-68865.herokuapp.com'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'

# Production configuration settings - relies on Heroku env variables
class ProductionConfig(Config):
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    APP_URL = 'https://vacation-rental-estimator-prod.herokuapp.com'
    AUTH0_CALLBACK_URL = APP_URL + '/callback'

