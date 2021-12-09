**Course Name: **CSCIE-14a: Building Interactive Web Applications
for Data Analysis

**Instructor:** Zona Kostic

**TA**: Gabe Korodi

**Group Assignment:** PWA - Price Prediction

**Members**: Andrew Fabrizio, Joe Pursel, Jing Yu

**App URL:** https://immense-mountain-68865.herokuapp.com/

**GitHub URL:** https://github.com/Fabrizio-Andrew/Vacation-Rental-Pricing-Estimator

**Screencast URL**: https://www.youtube.com/watch?v=c7xJrOAaWOs

**Project code download, with SQL dump**: https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/VacationGroup.zip



# Vacation Rental Pricing Helper

## Getting Started - Local dev

### Prerequisites
* Install Python 3 + pip

* Create a virtualenv and install dependencies
```bash
# Create virtual environment
$ python venv venv
# Install Dependencies
$ pip install -r requirements.txt
```

* Create secrets.json file
```bash
{
    "SECRET_KEY": "<YOUR_SECRET_KEY>",
    "DB_HOST": "localhost",
    "DB_HOST_PORT": "5432",
    "DB_USER": "<YOUR_USERNAME>",
    "DB_PASSWORD": "<YOUR_PASSWORD>",
    "DB_NAME": "postgres",
    "GOOGLE_API_KEY": "<YOUR_KEY"
}
```
### Setup DB

* Create postgres db in Docker
```bash
docker compose up
```

* Configure db
```bash
$ flask db init #(maybe not needed)
$ flask db stamp head
$ flask db migrate
$ flask db upgrade
```

NOTE: The DB will not have the required data to support the "Insights" tab.


## Getting Started - Heroku
(see https://devcenter.heroku.com/articles/creating-apps)

### Prerequisites

* Heroku CLI
(for macOS)
```bash
$ brew tap heroku/brew && brew install heroku
```

### Build & deploy

* Log in to Heroku
```bash
$ heroku login
```

* Create a Heroku app
```bash
$ heroku create
```

* Deploy to Heroku
```bash
$ git push heroku main
```

* Configure Env Variables

An environment variable must be set in Heroku for each of the values in secrets.json.

### Set up the Heroku DB

* Create the DB
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

* Configure the DB
```bash
$ heroku run flask db init #(maybe not needed)
$ heroku run flask db stamp head
$ heroku run flask db migrate
$ heroku run flask db upgrade
```

NOTE: The DB will not have the required data to support the "Insights" tab.


## App Overview

### Motivation

Property owners renting out on a short-term basis (hosts) often have little experience in the real estate or hospitality industries and lack the ability to accurately predict the fair market value of their short term rental. AirBnB offers a pricing estimator, but it can often be inaccurate.

The Vacation Rental Pricing Helper will provide hosts with a baseline prediction of the fair market value of their short-term rental based on location, property features, date, and any other predictors that the team finds to be meaningful. In addition, hosts will be provided with key data insights from listings data, alongside processed natural language insights. Armed with such information, hosts will be better prepared to accurately price their short-term rentals.



#### Homepage

On the homepage, user is greeted with a basic header, consisting of a **short description** and a pricing **heat map**, to inform the user of the **purpose of the site**. Once the user is engaged, they can **fill out a basic form** (designed such that as little effort as possible is required to complete) of their property information.

#### Homepage screenshot

![image-20211126151702236](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126151702236.png)



#### Results Page

After submission of the form, the user is taken to a **results page**. On that page, user would see a **zoomed in map**, in which the property location, **nearest subways**, and **nearest landmarks** are displayed and labeled. In addition, user sees an **overview of their submission** and the predicted pricing for their property. For the pricing, the page shows an interactive chart that tells **exactly which factor contributes in what dollar amounts to the final pricing.** 

#### Results Page Screenshot

![image-20211126153117181](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126153117181.png)



#### Insights Page

The insights page is where the user can **explore the datasets at will** with a range of filters. The available range of filters are **neighborhoods**, **super host status**, **response rate percentage**, and **host experience by years**.

After the user makes the selections and click the **FILTER** button, the page will inform the user that the results are being retrieved and analyzed.

There are **<u>two tabs/categories available for exploration.</u>**

The first is called **Insights**, which contains datas and charts that mostly concerns pricing, neighborhoods, room types, aggregated review scores, super host status, accommodates, and host experience.

The second is called **Reviews NLP.** The data presented from this tab is all derived and engineered from the existing reviews data. It informs of gender distribution among reviewers, distribution of positive, negative, and neutral reviews, polarity score (sentiment: -1 to 1) distribution of reviews, subjectivity distribution (how subjective a review is: 0 to 1),  20 most frequently used subjects in reviews, and 20 most frequently used adjectives in reviews. (MORE DETAILS and Notebook is included in the App Features - NLP section)

#### Insights Page Screenshots

![image-20211126153147025](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126153147025.png)

![image-20211126153251631](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126153251631.png)

## App Features in Details

### Interface

\- The interface is built primarily with the Bootstrap Framework.

\- Interactive DOM components utilizes Bootstrap built-in's, along with jQuery, and Javascript.

\- The app is designed to be responsive, optimized for mobile viewing and usage, as shown:

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126151820589.png" alt="image-20211126151820589" style="zoom:33%;" />

\- Additionally, D3.js is used for interactive components, visualizations, data processing and manipulation, and certain DOM elements manipulations.

\- Charts and graphs are primarily displayed using Plotly.js, which is built on D3.js and stack.gl. The data were manipulated/calculated first using D3.js and then handed off to Plotly, which renders the graphics interactive and visually appealing.

\- Chart.js for just one chart - Contributing Factors on the Results page

\- Google Places API for geocoding; allowing quick input of user address and converting user address to Longitude and Latitude. The API key has been restricted to app traffic, even as it is exposed in the javascript reference link.

\- The forms and fields that require user interaction were designed to minimize user effort.

### User Management

\- Sign up and login pages

\- used UserMixin from flask_login library to manage user session with users table

\- SHA256 password hashing and storage in PostgreSQL data table

\- Sha256 login authentication

\- Signup password field strength checking; email field validity checking

\- User dashboard and email verification were not implemented due to lack of useful features to implement user-wise; but could be easily implemented with the infrastructure in place

\- Following shows the PostgresSQL users table

![image-20211126151058604](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126151058604.png)

### Security

\- CRSF protection is enabled using CSRFProtect from flask_wtf library and by inserting CSRF tokens as a hidden field in form submissions.

\- Cookies protection

\- SQL Query Injection protection

### Progressive Web App (PWA)

\- ServiceWorker - service worker would cache resources and allow offline rendering. It was originally implemented but due to it caching CSRF tokens (leading to expired tokens), caching navigation bar (leading to user email not showing after login or not disappearing after log out), and sometimes caching of old charts on Insights page. Eventually, the service worker is implemented, but the offline assets caching feature were commented out for considerations of above problems and the fact that a lot of retrievals required internet access nevertheless.



![image-20211205230539692](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205230539692.png)

\- Icons of various sizes specified in **manifest.json**

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205225643297.png" alt="image-20211205225643297" style="zoom: 50%;" />

\- Desktop chrome installable (Mac, tested working under Chrome)

![image-20211205231352736](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205231352736.png)

\- IOS homescreen installable (Safari Add to Homescreen, tested working)

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075854995.png" alt="image-20211126075854995" style="zoom:50%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075934797.png" alt="image-20211126075934797" style="zoom: 50%;" />

\- Android homescreen installable (from Chrome, tested working)

\- PWA score of **170** from pwabuilder.com for https://vacation-group.herokuapp.com

![image-20211205230605383](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205230605383.png)

![image-20211205231525781](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205231525781.png)

![image-20211205231541210](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205231541210.png)

![image-20211205231556383](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205231556383.png)

### Database

\- Postgres database for storage and retrieval

\- Pandas read_sql and SQL Queries for querying the database within Python and processing using pandas dataframe

\- SqlAlchemy for ORM

\- 1.4 Millions rows in database, 10 tables, 232.7 MB

\- Some tables were duplicated and then modified.

\- 3 tables used in the end: **reviews_clone_fin, users, listings_postgres_clone3**; their structure is shown below

![image-20211126073011431](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126073011431.png)

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205232952716.png" alt="image-20211205232952716" style="zoom:33%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233010687.png" alt="image-20211205233010687" style="zoom:33%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233024782.png" alt="image-20211205233024782" style="zoom:33%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233207532.png" alt="image-20211205233207532" style="zoom:33%;" /><img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233227292.png" alt="image-20211205233227292" style="zoom:33%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233254805.png" alt="image-20211205233254805" style="zoom:33%;" /><img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205233307135.png" alt="image-20211205233307135" style="zoom:33%;" />

### Insights Page Detailed

\- Designed to allow users to see reports for data of choosing

\- Filters by specific neighborhood, super host status, response rate, host experience in years

\- **Aggregate Stats:** # of listings retrieved, mean price, median price, standard deviation, average rating

\- Violin plot of pricing by neighborhoods

\- Room Types and Price Violin Plots; Room Types Pie Chart

\-  Various Review Scores Radar Plot

\- Accommodates by Count (# of listings) and vs Price

\- Host # of Years by Count (# of listings) and vs Price

\- Charts and Graphs from **cleaned** dataset + **engineered** features, 79 columns

![image-20211126150938136](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126150938136.png)

### Natural Language Processing Detailed

\- [Download Notebook](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/VacationNLP.ipynb)

\- The most extensively used verb is the 'be' linking verb (is, was, are...)

\- The most extensively used sentence structure is therefore "subject + "be" + "adjective", eg. "the place was comfortable"

\- Given such, verbs are ignored during analysis

\- **Intent analysis** **was not performed** due to the reviews being uniform in intention: to inform

\- **Overwhelming majority of reviews were positive**; skewness raises the concern of validity

\- Used **SpaCy** to extract nouns(subjects) and adjectives from every review, aggregated them for insights

\- Used **OpenAI** **ada**(simple, cheap) **engine** to label the reviewers' names by gender, for demographic insight

\- Originally attempted to use openAI's **davinci-instruct-beta-v3** engine to label the reviews as such:

```
Location: 4/5

Cleanliness: 4/5

Amenities: 3/5

Value: 4/5
```

which would provide more detailed insights (even if without the numerical label), but the attempt has proven to be **cost prohibitive**;

\- A rough estimate places final cost for at least over $2000 for the entire dataset of ~100k reviews for 1600 listings

\- Final Reviews Dataset with NLP features

![image-20211126150815715](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126150815715.png)



### Bugs/Problems

\- ~~By caching resources using a service worker, when the user signs out, the user email is still cached in display and would sometimes require an addition refresh to clear; similar for logging in. In the same manner, the CSRF token would expire before the cached page has a chance to refresh the token, leading to a page that displays "The CSTF token has expired"~~

\- The above bug have been solved with the removal of offline availability in PWA's service worker.



## Modeling

\- Cleaning data, standardizing, removing outliers

\- Feature selection

\- Feature engineering: host years, closeness to landmarks, closeness to subways

\- **Final Model: Linear Regression**; chosen out of simplicity, explainability, interpretability; others were considered and modeled but eventually discarded.

![image-20211126153027132](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126153027132.png)

#### Discarded models

- **Neural network:** overfit, not enough data given the number of features, lacking interpretability
- ![image-20211126152230235](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126152230235.png)
- **Random Forest**: not enough improvement over the linear regression model to trade for simplicity and explainability, even after grid search
- ![image-20211126152519673](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126152519673.png)
- **XGboost** - same as above
- ![image-20211126152549918](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126152549918.png)

- **Decision tree** - lacking significant improvement 

![output](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/output.svg)



#### Notebooks for EDA, feature engineering, and modeling:

https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda4calendar.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda3model.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda2.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda1.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda0.ipynb



## Additional Considerations

#### Dataset Problems

\- The datasets used was from http://insideairbnb.com/. They scrape their data and therefore is a non-direct source of data

\- Original, first-hand data from AirBnB itself is not available due to Airbnb's restrictions

\- Reviews data extremely biased towards the positive - questioning the integrity of AirBnB displayed reviews.

\- Calendar data is forward looking, and not historical

\- No transactional data - pricing predicting is therefore only based on hosts' arbitrary pricing, and not actual sales prices.

\- Availability data was  also elusive because it was impossible to determine whether a listing was unavailable on any particular day due to host making it unavailable or that it was booked by an actual renter.

#### Calendar Feature (Discarded)

\- Original proposition shown

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/calendar_feature.png" alt="calendar_feature" style="zoom:67%;" />

\- Dataset for such feature was prepared and engineered. Days of week and holidays are considered. shown below; 

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075100717.png" alt="image-20211126075100717" style="zoom:50%;" />

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075136514.png" alt="image-20211126075136514" style="zoom:50%;" />

![image-20211126075239980](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075239980.png)

\- Calendar feature is eventually **NOT implemented** due to the consideration of the fact that the entire calendar dataset is based on AirBnB's forward predictions (Jul 2021 to Jul 2022) [look at dates]

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126151016081.png" alt="image-20211126151016081" style="zoom:50%;" />

\- Predicting based on predictions would mean error on errors

\- **IF**, with historical, transactional data available, such an implementation would be much more useful

#### Image Analysis, CNN (Not implemented)

\- Potential image analysis methods were considered

\- Image resolution analysis: since images are taken by professional photographers, so high resolution is almost a uniform feature, lacking significant differentiability.

\- 'image appeal': lacking a useful, labeled dataset for such metric

\- Other subjective metrics, such as how spacious a property feels and how clean it is, are considered, but not implemented due to the same constraints as above

## APP Code Structure

### Folder Structures

![image-20211205235656049](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211205235656049.png)

#### Non-Production folders

- **experimentation** - included raw, processed datasets, data files, and notebooks used during EDA, features engineering/selection, modeling, Postgres experimentations and notebooks
- **d3 experiments** - included an initial prototype of a d3 heatmap
- **NLP_Notebook_and_data** - notebook and data used during NLP analysis and feature engineering
- **data** - many are duplicates from the experimentation, some are additionally engineered or processed. Includes,
  - List of subways in Boston
  - List of landmarks in Boston
  - MBTA's data on various modes of transportations, stations, etc...
  - InsideAirbnb's original data: calendar, listings, and reviews
  - InsideAirbnb's data after processing
  - Processed data: neighborhoods prices, 
  - Neighborhoods' geojson data for d3 heatmap
  - Processed data from calendar data, including seasonality, days of week, holidays
  - Standardizations and means data

- Within the **data** folder, there exists a SQL dump of the entire Postgres database, **d1gel5ia1af8fe.sql**, that is used in production. It is 197 MB. 



#### Production Folders

- **ROOT**
  - **routes.py** - Flask routing, more details below
  - **Project Plan.md** - original project plan proposal
  - **Procfile** - "web:  gunicorn routes:app"
  - **model.py** - specifies User class which inherits UserMixin and SqlAlchemy Model; this allows connection to the users table in Postgres to add, authenticate users and create sessions
  - **manifest.json** - for PWA: specifies app name, short name, description, theme colors, scope, and icons
  - **runtime.txt** - specifies python runtime for heroku - "python-3.9.6"
  - **requirements.txt**
    - <img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206001614667.png" alt="image-20211206001614667" style="zoom: 33%;" />
- **static**
  - **img**, **svg** - icons and svgs used on web app
  - **Js** - bootstrap's js file, chart.js, topojson.js, jquery.js
  - **Css** - bootstrap css and custom stylesheets
- **templates**
  - index.html - homepage, contains heatmap, form, description
  - layout.html - header, footer, dependencies, meta tags
  - signup.html / login.html
  - results_page.html
  - insights.html
  - about.html
  - 404.html 
  - 401.html



#### <u>routes.py</u> detailed

- **Dependencies** and flask **app settings**, setup **database** connection, secret key, login manager, CSRF protections, cookies protection,
  - ![image-20211206002302304](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206002302304.png)

- More setup - including **specifying paths** to subways data and landmarks data in Boston

  - Since **the linear model and data is extremely lightweight**, they are simply loaded here for ease and quick of access.

  ![image-20211206002453595](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206002453595.png)

- **User Management**: Login and logout, signup, password validation

  - ![image-20211206002603167](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206002603167.png)

  - ![image-20211206002721941](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206002721941.png)

- **Index and about pages** - simply renders template pages

  - ![image-20211206002814016](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206002814016.png)

- **Results Page:**

  - Process user submission for the linear model, calculate baseline pricing, calculate closest landmarks, calculate closest subways, return results as variables for jinja template
  - ![image-20211206021009591](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021009591.png)

- **Error Handling:** 

  - ![image-20211206021038105](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021038105.png)

- Insights Page -  renders page template, with API calls to backend

  - ![image-20211206021112496](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021112496.png)

  - Query listings data and returns records as json to frontend:<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021207158.png" alt="image-20211206021207158" style="zoom: 50%;" />

    ![image-20211206021219092](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021219092.png)

  - Query reviews NLP data and return records as js to frontend:

    - ![image-20211206021346221](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021346221.png)

- Utilities
  - ![image-20211206021408446](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211206021408446.png)

