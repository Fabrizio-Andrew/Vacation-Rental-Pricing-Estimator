import os
import json

# An environment variable for "ENVIRONMENT" must be set to "staging", or "production" for those
# environments. If environment = "staging" or "production", env variables for AUTH0_CLIENT_ID 
# & AUTH0C_CLIENT_SECRET are also required.

if os.environ.get('ENVIRONMENT') == 'staging':
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    APP_URL = 'https://immense-mountain-68865.herokuapp.com'

elif os.environ.get('ENVIRONMENT') == 'production':
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    APP_URL = 'https://vacation-rental-estimator-prod.herokuapp.com'

else:
    f = open('secrets.json')
    secrets = json.load(f)
    
    AUTH0_CLIENT_ID = secrets['AUTH0_CLIENT_ID']
    AUTH0_CLIENT_SECRET = secrets['AUTH0_CLIENT_SECRET']
    APP_URL = 'http://localhost:5000'

API_BASE_URL = 'https://dev-l0m79glj.us.auth0.com'
AUTH0_ACCESS_TOKEN_URL = API_BASE_URL + '/oauth/token'
AUTH0_AUTHORIZE_URL = API_BASE_URL + '/authorize'
AUTH0_CALLBACK_URL = APP_URL + '/callback'
AUTH0_CLIENT_KWARGS = {
    'scope': 'openid profile email'
}