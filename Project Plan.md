# Project Plan

**Dataset** - primarily using dataset from InsideAirbnb

**Primary Objective** - uncover patterns within datasets through statistical and machine learning methods, then yielding a PWA that could allow end users (property owners) to accurately set rental pricing for maximum revenue, whilst getting tips on how to do so. 

## Steps and Timelines

### Preprocessing

1. Data Cleansing - detecting incomplete and inaccurate records; modifying, deleting, and replacing entries, focusing on making the data usable for following analysis and modeling

   - Normalize numerical features 

   - Removing certain outliers

2. Feature Extraction and Feature Engineering

   - binary encoding, one-hot encoding categorical features
   - Engineer additional features, either calculated using existing features or newly developed using external dataset; some possibilities: 
     - From host_since date data to host_number_of_years
     - Closeness to Landmarks
   - PCA, tSNE for getting most relevant features

### Modeling

1. Modeling - with primary objective and end user in mind, construct models that lean towards explainability and ease of use, as opposed to perhaps accuracy.
   - Decision Trees, multivariate regression > neural networks, random forests

### Deployment

1. Database

   - Put engineered data files onto a Postgres database, link it to flask application for later retrieval.

2. User Interface (webpage):

   - Objective: ease of use, intuitive, interactive.

   - bootstrap for UI;
   - D3.js for interactivity and data visualization, potentially including, not limited to heat maps and word clouds.

### Timeline

- 2 weeks for preprocessing, EDA, and feature extraction/engineering

- 2 weeks for modeling and EDA

- Remaining weeks for deployment, UI, Database setup

### Duties and Roles

- Duties and roles are flexible and assigned as the project goes



