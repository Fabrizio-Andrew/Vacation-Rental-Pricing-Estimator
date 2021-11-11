import os
from flask import Flask, request, make_response, render_template, session, redirect, url_for
import json
from authlib.integrations.flask_client import OAuth
from functools import wraps
from six.moves.urllib.parse import urlencode

from standardization import standardize, destandardizePrice, standards
from linearmodel import coefs, bias
from percentile import calculatePercentile
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.AUTH0_CLIENT_SECRET
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id = config.AUTH0_CLIENT_ID,
    client_secret = config.AUTH0_CLIENT_SECRET,
    api_base_url=config.API_BASE_URL,
    access_token_url=config.AUTH0_ACCESS_TOKEN_URL,
    authorize_url=config.AUTH0_AUTHORIZE_URL,
    client_kwargs=config.AUTH0_CLIENT_KWARGS
)

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=config.AUTH0_CALLBACK_URL)


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'YOUR_CLIENT_ID'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated


@app.route('/user_dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/estimate', methods=['POST'])
def estimate():
    if request.method == 'POST':
        
        # Collect and standardize user data
        data = json.loads(request.get_data('body'))
        standardizeddata = standardize(data)

        # Find the dot product of standardized user data and regression model coefficients
        dotproduct = sum(standardizeddata[key] * coefs.get(key, 0) for key in standardizeddata)

        # add the bias
        estimatez = dotproduct + bias
        
        # destandardize the price
        estimate = destandardizePrice(estimatez)

        # Calculate the percentile of the price estimate from z-score
        percentile = calculatePercentile(estimatez)
       
        # Create the response object
        responsepayload = {
            'estimate': round(estimate, 0),
            'percentile': round(percentile * 100, 0),
            'recommendations': []
        }
        # Check for recommendations
        if standardizeddata['host_resp_over_few_days'] == 1:
            responsepayload['recommendations'].append('response_time')
        if standardizeddata['dist_to_landmark'] < standards['dist_to_landmark']['mean']:
            responsepayload['recommendations'].append('landmark')

        response = make_response(responsepayload)

        print(response)
        return response

if __name__ == '__main__':
    app.run(debug=True)