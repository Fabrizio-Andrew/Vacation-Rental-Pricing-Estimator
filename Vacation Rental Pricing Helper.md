**Course Name: **CSCIE-14a: Building Interactive Web Applications
for Data Analysis

**Instructor:** Zona Kostic

**TA**: Gabe Korodi

**Group Assignment:** PWA - Price Prediction

**Members**: Andrew Fabrizio, Joe Pursel, Jing Yu

## Vacation Rental Pricing Helper

Property owners renting out on a short-term basis (hosts) often have little experience in the real estate or hospitality industries and lack the ability to accurately predict the fair market value of their short term rental. AirBnB offers a pricing estimator, but it can often be inaccurate.

The Vacation Rental Pricing Helper will provide hosts with a baseline prediction of the fair market value of their short-term rental based on location, property features, date, and any other predictors that the team finds to be meaningful. In addition, hosts will be provided with key data insights from listings data, alongside processed natural language insights. Armed with such information, hosts will be better prepared to accurately price their short-term rentals.

### App Overview

On the homepage, user is greeted with a basic header, consisting of a short description and a pricing heat map, to inform the user of the purpose of the site. Once the user is engaged, they can fill out a basic form (designed such that as little effort as possible is required to complete) of their property information.

After submission of the form, the user is taken to a results page. On that page, user would see a zoomed in map, in which the property location, nearest subways, and nearest landmarks are displayed and labeled. In addition, user sees an overview of their submission and the predicted pricing for their property. For the pricing, the page shows an interactive chart that tells exactly which factor contributes in what dollar amounts to the final pricing.

On the insights page, user can explore the dataset at will with a range of filters. User is presented with a number of charts and data insights.

## App Features

### Interface

\- Bootstrap CSS/JS

\- Html, jQuery, Javascript

\- Responsive design

\- D3.JS for interative components, visualizations, data processing, and DOM manipulations

\- Plot.ly for interactive plots, handoff from D3

\- Chart.js for just one chart

\- Google Places API for geocoding (api restricted by domain)

\- User experience design with simplified form

### User Management

\- Sign up and login

\- Sha256 password hashing and storage in postgres data table

\- Sha256 login authentication

\- Signup password field strength checking; email field validity checking

\- User dashboard not implemented due to lack of useful features to implement user-wise; but could be easily implemented with the infrastructure in place

### Security

\- CSRF protection is enabled.

\- Cookies protection

\- SQL Query Injection protection (under development)

### PWA

\- Offline Loading, **Service Worker,** Caching of Resources

\- Icons of various sizes specified in **manifest.json**

\- Desktop chrome installable (Chrome, tested working)

\- IOS homescreen installable (Safari, tested working)

\- Android homescreen installable (Chrome, tested working)

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075854995.png" alt="image-20211126075854995" style="zoom:50%;" /><img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075934797.png" alt="image-20211126075934797" style="zoom: 50%;" />

### Database

\- Postgres database for storage and retrieval

\- Pandas SQL Queries for python processing

\- Sqlalchemy for ORM

![image-20211126073011431](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126073011431.png)

### Insights Page

\- Designed to allow users to see reports for data of choosing

\- Filters by neighborhood, super host status, response rate, host experience in years

\- Aggregate Stats: mean price, median price, standard deviation, average rating

\- Violin plot by neighborhoods

\- Room Types and Price Violin Plots; Room Types Pie Chart

\-  Various Review Scores Radar Plot

\- Accommodates by Count and vs Price

\- Host # of Years by Count and vs Price



### Natural Language Processing

\- [Download Notebook](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/VacationNLP.ipynb)

\- The most extensively used verb is the 'be' linking verb (is, was, are...)

\- The most extensively used sentence structure is therefore "subject + "be" + 

"adjective", eg. "the place was comfortable"

\- Given such, verbs are ignored during analysis

\- **Intent analysis** was not performed due to the reviews being too uniform in intention: to inform

\- **Overwhelming majority of reviews were positive**; skewness raises the concern of validity

\- Used **SpaCy** to extract nouns(subjects) and adjectives from every review, aggregated them for insights

\- Used **OpenAI** **ada**(simple, cheap) **engine** to label the reviewers by gender, for demographic insight

\- Originally used openAI's **davinci-instruct-beta-v3** engine to label the reviews as such:

```
Location: 4/5

Cleanliness: 4/5

Amenities: 3/5

Value: 4/5
```

which would provide more detailed insights (even if without the numerical label), but the attempt has proven to be **cost prohibitive**;

\- A rough estimate places final cost at around $2000 for the entire dataset of ~100k reviews for 1600 listings



### Bugs/Problems

\- By caching resources using a service worker, when the user signs out, the user email is still cached in display and would sometimes require an addition refresh to clear; similar for logging in. In the same manner, the CSRF token would expire before the cached page has a chance to refresh the token, leading to a page that displays "The CSRF token has expired"



## Modeling

\- cleaning data, standardizing, removing outliers

\- feature selection

\- feature engineering: host years, closeness to landmarks, closeness to subways

#### Notebooks:

https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda4calendar.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda3model.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda2.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda1.ipynb
https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/eda0.ipynb



## Other Considerations

#### Dataset

​    \- Non-direct source of data; scraped data; original data is not available

​    \- Reviews data extremely biased towards the positive - questioning the integrity of AirBnB.

​    \- First-hand data is not accessible due to AirBnB's lack of openness

​    \- Calendar data is forward looking

​    \- No transactional data

#### Calendar Feature

\- Original proposition shown

![calendar_feature](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/calendar_feature.png)

\- Dataset for such feature was prepared and engineered. Days of week and holidays are considered. shown below; 

<img src="https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075100717.png" alt="image-20211126075100717" style="zoom:50%;" />

![image-20211126075136514](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075136514.png)

![image-20211126075239980](https://myimagesjingyu.s3.us-west-2.amazonaws.com/upic/image-20211126075239980.png)

\- calendar feature is eventually **NOT implemented** due to the consideration of the fact that the entire calendar dataset is based on AirBnB's forward predictions (Jul 2021 to Jul 2022)

\- predicting based on predictions = error on errors

\- **IF**, with historical, transactional data available, such an implementation would be much more useful



#### Image Analysis, CNN

\- Potential image analysis methods considered

\- Image resolution analysis: images are taken by professional photographers, so high resolution is uniform, lacking differentiability

\- 'image appeal': lacking a useful, labeled dataset for such metric

\- Other subjective metrics, such as how spacious a property feels and how clean it is, are considered, but not implemented due to constraints

