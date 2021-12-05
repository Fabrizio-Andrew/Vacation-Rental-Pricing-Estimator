from flask import Flask, make_response,render_template, request, redirect, url_for, flash, jsonify, send_file,send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import geopy.distance
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import simplejson as json
from models import User, db
from passlib.hash import sha256_crypt as sha256
import re
from os import environ

app = Flask(__name__)
app.config.from_object(f'config.{os.environ["APP_SETTINGS"]}')


csrf = CSRFProtect()
csrf.init_app(app)
app.config['CUSTOM_STATIC_PATH'] = app.root_path + '/data/'
# app.config['WTF_CSRF_TIME_LIMIT'] = None
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# production_db_uri1 = environ.get('HEROKU_POSTGRESQL_WHITE_URL').replace("postgres://", "postgresql://")
# production_db_uri0 = environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
# app.secret_key = os.environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = production_db_uri0

# DATABASE_URI_NEW = environ.get('HEROKU_POSTGRESQL_WHITE_URL').replace("postgres://", "postgresql://")
# "postgresql://dbudyqehphowvj:ce19f33d1898777e99ec500d4651375b6deb8f98bb8d4caa5a3254e97126e527@ec2-34-198-189-252.compute-1.amazonaws.com:5432/d1gel5ia1af8fe"


# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI_NEW
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.secret_key = environ.get('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)

db_query = create_engine(app.config['SQL_URL'])

sites_data_path = "data/sites_boston.csv"
subway_data_path = "data/transport/subway.json"
coefs=np.array([-0.18180501, -0.32107893, -0.36701204, -0.15250934, -0.05541475,
       -0.03938244,  0.55789099,  0.01080494,  0.10483031,  0.25154944,
        0.39175801])
bias = 0.12633143197779734


with open("data/processed/boston_processed_mean.json") as f:
    all_means = json.load(f)
with open("data/processed/boston_processed_std.json") as s:
    all_stds = json.load(s)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(uid=user_id).first()

@app.route('/sw.js')
def sw():
    return send_from_directory(app.root_path, 'static/sw.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.root_path, 'manifest.json')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if sha256.verify(request.form['password'], user.password):
                login_user(user) # remember=True, duration=datetime.timedelta(days=1)
                # remember = request.form['remember']
                return redirect(url_for('index'))
            else:
                return render_template('login.html', message='Wrong email or password!')
        return render_template('login.html', message='Wrong email or password!')
    return render_template('login.html')


@app.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            return render_template('signup.html', message='''<div class="alert alert-warning" role="alert">Email already exists! Please <a href='/login'>Login</a> </div>''')
        else:
            email = request.form['email']
            password = request.form['password']
            if password_validation(password):
                pass
            else:
                return render_template('signup.html',
                message='''<div class="alert alert-warning" role="alert">Password must contain 6-20 characters, one uppercase letter, one lowercase letter, one number and one special character</div>''')
            # if email_validation(email):
            #     pass
            # else:
            #     return render_template('signup.html',
            #     message='''<div class="alert alert-warning" role="alert">Email Invalid!</div>''')
            user = User(email=email, password=sha256.hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return render_template('signup.html', message='''<div class="alert alert-success" role="alert">Signup successful! You will be redirected shortly! Or Click <a href='/'>Here</a></div>
                        <script>setTimeout(function(){window.location.href = '/';}, 2000);</script>''')
    else:
        return render_template('signup.html')

def password_validation(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    match = re.search(pat, password)
    if match:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/results_page', methods=['GET', 'POST'])
def results_page():
    if request.method == 'POST':
        # HostResponseTime 0hour 1hours 2day 3days 
        # RoomType 0private 1 hotel 2 shared 3 entire
        RoomTypeMap={0:"a Private Room", 1:"a Hotel Room", 2:"a Shared Room", 3:"an Entire Home/Apt"}
        HostResponseTimeMap = {0:"Within an Hour", 1:"Within a few Hours", 2:"Within a Day",3:"A Few Days or More" }
        
        HostResponseTime = int(request.form['HostResponseTime'])
        RoomType = int(request.form['RoomType'])
        Beds = int(request.form['Beds'])
        Accommodates = int(request.form['Accommodates'])
        Longitude = float(request.form['Longitude'])
        Latitude = float(request.form['Latitude'])
        # place_id = request.form['place_id']
        ReviewScore = float(request.form['ReviewScore'])

        user_submission = {"AutoAddress":request.form['AutoAddress'],"HostResponseTime": HostResponseTime, "RoomType": RoomType,
                         "Beds": Beds, "RoomTypeMap":RoomTypeMap[RoomType], "HostResponseTimeMap":HostResponseTimeMap[HostResponseTime],
                            "Accommodates": Accommodates, "Longitude": Longitude, "Latitude": Latitude, "ReviewScore": ReviewScore}
        closest_landmarks_list, closeness_to_landmark = GetClosestLandmarksList(Latitude, Longitude)
        closest_subways_list, closeness_to_subway = GetClosestSubwaysList(Latitude, Longitude)

        # calculate model predictions 
        # present model variables and weights
        model_input = [0]*11
        if(HostResponseTime==3):
            model_input[0]=1
        elif(HostResponseTime==2):
            model_input[3]=1
        elif(HostResponseTime==1):
            model_input[8]=1
        if(RoomType==0):
            model_input[2]=1
        elif(RoomType==1):
            model_input[6]=1
        model_input_pre_standardization = model_input
        model_input[1]= (closeness_to_landmark-all_means['closeness_to_landmark'])/all_stds['closeness_to_landmark']
        model_input[4] = (Longitude - all_means['longitude'] )/all_stds['longitude']
        model_input[5] = (Latitude - all_means['latitude'] )/all_stds['latitude']
        model_input[7] = (ReviewScore - all_means['review_scores_rating'] )/all_stds['review_scores_rating']
        model_input[9] = (Beds - all_means['beds'] )/all_stds['beds']
        model_input[10] = (Accommodates - all_means['accommodates'] )/all_stds['accommodates']
        model_output = np.dot(model_input,coefs) + bias
        model_output = model_output*all_stds['price'] + all_means['price']


        # get labels and weights and logic for Contributing Factors chart
        features = ['Response Time >= 1 Day', # binary
            'Closeness to Landmarks',
            'Private Room', # binary
            'Response Time < 1 Day', # binary
            'Longitude',
            'Latitude',
            'Hotel Room', # binary
            'Overall Review Score',
            'Response Within a Few Hours', # binary
            '# of Beds',
            'Accommodates']
        # zipped_label_weight = []
            # for i, d in enumerate(model_input):
            #     if(d!=0):
            #         zipped_label_weight.append((features[i],list(coefs)[i]))
            #         zipped_label_weight.sort(key=lambda x: x[1], reverse=True)
            # chart_labels = [x[0] for x in zipped_label_weight]
            # chart_weights_data = [x[1] for x in zipped_label_weight]
            # positive_color = 'rgba(255, 99, 132, 1)'
            # negative_color = 'rgba(54, 162, 235, 1)'
            # chart_colors=[]
            # for i in chart_weights_data:
            #     if(i>0):
            #         chart_colors.append(positive_color)
            #     else:
            #         chart_colors.append(negative_color)

        # get labels and weights and logic for Contributing Factors chart
        zipped_label_weight = []
        for i, d in enumerate(model_input):
            if(d!=0):
                zipped_label_weight.append((i, features[i],list(coefs)[i]*model_input[i]))
                zipped_label_weight.sort(key=lambda x: x[2], reverse=True)
        chart_labels = [x[1] for x in zipped_label_weight]
        chart_weights_data = [x[2]*120.7497 for x in zipped_label_weight]
        positive_color = 'rgba(255, 99, 132, 1)'
        negative_color = 'rgba(54, 162, 235, 1)'
        chart_colors=[]
        for i in chart_weights_data:
            if(i>0):
                chart_colors.append(positive_color)
            else:
                chart_colors.append(negative_color)

        # if time permits; present and do word cloud data

        return render_template('results_page.html', title="Results",
            closest_landmarks_list=closest_landmarks_list,
            closest_subways_list=closest_subways_list,
            closeness_to_landmark=closeness_to_landmark,
            closeness_to_subway=closeness_to_subway,
            user_submission=user_submission,
            model_input=model_input,
            model_output=model_output,
            coefs=list(coefs),
            bias=bias,
            all_means=all_means,
            all_stds=all_stds,
            chart_labels=chart_labels,
            chart_weights_data=chart_weights_data,
            chart_colors=chart_colors,
            )
    else:
        return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def unauthorized_user(e):
    return render_template('401.html'), 401


@app.route('/insights')
def insights():
    return render_template('insights.html', title="Insights")

@app.route('/query')
def queryDatabase():
    # https://realpython.com/prevent-python-sql-injection/
    # db_query = create_engine(DATABASE_URI_NEW)
    initial_query = "SELECT * FROM listings_postgres_clone3 "
    neighbourhood  = request.args.get('neighbourhood', None)
    # strip quotes from neighbourhood
    superhost  = request.args.get('superhost', None)
    response_rate = request.args.get('response_rate', None)
    host_years = request.args.get('host_years', None)

    # room_type  = request.args.get('room_type', None)
    # min_price  = request.args.get('min_price', None)
    # max_price  = request.args.get('max_price', None)
    # min_beds  = request.args.get('min_beds', None)
    # max_beds  = request.args.get('max_beds', None)
    # min_accommodates  = request.args.get('min_accommodates', None)
    # max_accommodates  = request.args.get('max_accommodates', None)
    # min_review_scores_rating  = request.args.get('min_review_scores_rating', None)
    # max_review_scores_rating  = request.args.get('max_review_scores_rating', None) 

    all_criteria = [neighbourhood, superhost, response_rate, host_years]
    # all_criteria is not None
    first_criteria = True
    if any(all_criteria):
        initial_query += "WHERE "
        if neighbourhood:
            if first_criteria:
                initial_query += "neighbourhood_cleansed='" + neighbourhood + "'"
                first_criteria = False
            else:
                initial_query += " AND neighbourhood_cleansed='" + neighbourhood + "'"
        if superhost:
            if first_criteria:
                initial_query += "host_is_superhost='" + superhost + "'"
                first_criteria = False
            else:
                initial_query += " AND host_is_superhost='" + superhost + "'"
        if response_rate:
            if first_criteria:
                initial_query += "host_response_rate >= '" + str(response_rate) + "'"
                first_criteria = False
            else:
                initial_query += " AND host_response_rate >= '" + str(response_rate) + "'"
        if host_years:
            if first_criteria:
                initial_query += "host_number_of_years >= '" + str(host_years) + "'"
                first_criteria = False
            else:
                initial_query += " AND host_number_of_years >= '" + str(host_years) + "'"

    sql_df = pd.read_sql(
    initial_query,
    con=db_query
    )
    # print(initial_query)
    return sql_df.to_json(orient='records')

@app.route('/query_reviews', methods=['POST'])
def query_reviews():
    if request.method == 'POST':
        post_body = request.get_json()
        listing_id = str(post_body['listing_id']).strip("[]")

        # print(listing_id)
        sql_df = pd.read_sql(
        "SELECT * FROM reviews_clone_fin WHERE listing_id in (" + listing_id + ")",
            con=db_query
        )
        # keep only the columns we need
        sql_df = sql_df[['polarity', 'subjectivity','reviewer_gender','nouns','adjectives']] #comments
        return sql_df.to_json(orient='records')
    # query from reviews table and put into pandas dataframe



@app.route('/data/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename)



def RMeanSquared(list_distances):
    output = []
    for i in list_distances:
        output.append(i**2)
    return np.sqrt(np.mean(output))

def RMeanSquared_from_tuple(list_distances):
    output = []
    for idx,i in list_distances:
        output.append(i**2)
    return np.sqrt(np.mean(output))



def GetClosestSubwaysList(Latitude, Longitude):
    closest_subways_list=[]
    dist_to_each_subway = []
    with open(subway_data_path) as f:
        subway_data = json.load(f)['data']
        for idx, i in enumerate(subway_data):
            long1 = float(i['attributes']['longitude'])
            lat1 = float(i['attributes']['latitude'])
            dist_to_each_subway.append((idx, geopy.distance.distance((Latitude, Longitude),(lat1, long1)).km))
    dist_to_each_subway.sort(key=lambda x: x[1], reverse=False)
    closest_five = dist_to_each_subway[0:5]
    for i, (idx, dist) in enumerate(closest_five):
        subway = subway_data[idx]['attributes']['name']
        subway_id = subway_data[idx]['id']
        latitude = subway_data[idx]['attributes']['latitude']
        longitude = subway_data[idx]['attributes']['longitude']
        description = subway_data[idx]['attributes']['description']
        platform_name = subway_data[idx]['attributes']['platform_name']
        municipality = subway_data[idx]['attributes']['municipality']
        to_append=  { "subway": subway, "id": subway_id, "latitude": latitude,"longitude": longitude,  "distance":dist, "description": description, "platform_name": platform_name, "municipality": municipality}
        closest_subways_list.append(to_append)
    closeness_to_subway = RMeanSquared_from_tuple(closest_five)
    return closest_subways_list, closeness_to_subway



def GetClosestLandmarksList(Latitude, Longitude):
    # calculalte distance to landmarks
    sites_data = pd.read_csv(sites_data_path)
    landmarks=sites_data["Place"]  # Place,Address,Website,Latitude,Longitude
    landmarks_address = sites_data["Address"]
    landmarks_website = sites_data["Website"]
    landmarks_lats = sites_data["Latitude"]
    landmarks_longs = sites_data["Longitude"]
    dist_to_each_landmark = []
    lat2,long2 = Latitude,Longitude
    for idx, landmark in enumerate(landmarks):
        lat1,long1 = landmarks_lats[idx],landmarks_longs[idx]
        dist_to_each_landmark.append((idx, geopy.distance.distance((lat1, long1),(lat2, long2)).km))
    # sort by distance to each landmark
    dist_to_each_landmark.sort(key=lambda x: x[1], reverse=False)
    closest_five = dist_to_each_landmark[0:5]
    closest_landmarks_list = []
    for i, (idx, dist) in enumerate(closest_five):
        landmark = landmarks[idx]
        address = landmarks_address[idx]
        website = landmarks_website[idx]
        latitude = landmarks_lats[idx]
        longitude = landmarks_longs[idx]
        to_append=  { "landmark": landmark, "address": address, "website": website, "latitude": latitude,"longitude": longitude,  "distance":dist}
        closest_landmarks_list.append(to_append)
    closeness_to_landmark = RMeanSquared_from_tuple(closest_five)
    return closest_landmarks_list, closeness_to_landmark


if __name__ == '__main__':
    app.run(debug=True)