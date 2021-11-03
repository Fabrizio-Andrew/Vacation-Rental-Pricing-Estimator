standards = {
    "host_number_of_years": {
        "mean": 5.5168850506,
        "std": 2.8622682784
    },
    "host_verifications": {
        "mean": 5.5108695652,
        "std": 2.0612676632
    },
    "host_response_rate": {
        "mean": 95.1775362319,
        "std": 14.3360152041
    },
    "host_acceptance_rate": {
        "mean": 86.9329710145,
        "std": 21.7741990919
    },
    "latitude": {
        "mean": 42.3364447574,
        "std": 0.0277001004
    },
    "longitude": {
        "mean": -71.0806171689,
        "std": 0.0307066515
    },
    "accommodates": {
        "mean": 3.3260869565,
        "std": 2.3095641215
    },
    "amenities": {
        "mean": 29.8756038647,
        "std": 9.2550426982
    },
    "minimum_nights": {
        "mean": 21.6805555556,
        "std": 38.8893077352
    },
    "beds": {
        "mean": 1.7801932367,
        "std": 1.4261244756
    },
    "availability_30": {
        "mean": 0.2673309179,
        "std": 0.318287148
    },
    "availability_60": {
        "mean": 0.3496678744,
        "std": 0.3212691825
    },
    "availability_90": {
        "mean": 0.4057501342,
        "std": 0.3229033433
    },
    "availability_365": {
        "mean": 0.4681126332,
        "std": 0.3325968779
    },
    "number_of_reviews": {
        "mean": 59.2783816425,
        "std": 86.549752264
    },
    "review_scores_rating": {
        "mean": 4.6635326087,
        "std": 0.438185378
    },
    "review_scores_accuracy": {
        "mean": 4.7363103865,
        "std": 0.4293810317
    },
    "review_scores_cleanliness": {
        "mean": 4.7260386473,
        "std": 0.4069837571
    },
    "review_scores_checkin": {
        "mean": 4.8330797101,
        "std": 0.3742512311
    },
    "review_scores_communication": {
        "mean": 4.7997041063,
        "std": 0.4255231399
    },
    "review_scores_location": {
        "mean": 4.7554528986,
        "std": 0.3548732469
    },
    "review_scores_value": {
        "mean": 4.6022826087,
        "std": 0.4365356419
    },
    "dist_to_subway": {
        "mean": 1.2999911063,
        "std": 1.2812506367
    },
    "dist_to_landmark": {
        "mean": 2.24593516,
        "std": 2.0306119197
    },
    "price": {
        "mean": 167.2995169082,
        "std": 120.7497210335
    }
}

def standardize(data):
    standardizeddata = {}
        
    hostresp = data.get('host_resp', '')
    if hostresp == 'hours':
        standardizeddata['host_resp_over_few_days'] = 0
        standardizeddata['host_resp_under_day'] = 1
        standardizeddata['host_response_under_hours'] = 1
    elif hostresp == 'day':
        standardizeddata['host_resp_over_few_days'] = 0
        standardizeddata['host_resp_under_day'] = 1
        standardizeddata['host_response_under_hours'] = 0
    elif hostresp == 'over':
        standardizeddata['host_resp_over_few_days'] = 1
        standardizeddata['host_resp_under_day'] = 0
        standardizeddata['host_response_under_hours'] = 0
    
    roomtype = data.get('room_type', '')
    if roomtype == 'hotel':
        standardizeddata['room_type_hotel'] = 1
        standardizeddata['room_type_private'] = 0
    elif roomtype == 'private':
        standardizeddata['room_type_hotel'] = 0
        standardizeddata['room_type_private'] = 1
    else:
        standardizeddata['room_type_hotel'] = 0
        standardizeddata['room_type_private'] = 0
    
    standardizeddata['latitude'] = (data.get('latitude', '') - standards['latitude']['mean']) / standards['latitude']['std']
    standardizeddata['longitude'] = (data.get('longitude', '') - standards['longitude']['mean']) / standards['longitude']['std']
    standardizeddata['dist_to_landmark'] = (data.get('dist_to_landmark', '') - standards['dist_to_landmark']['mean']) / standards['dist_to_landmark']['std']
    standardizeddata['review_scores_rating'] = (data.get('review_scores_rating', '') - standards['review_scores_rating']['mean']) / standards['review_scores_rating']['std']
    standardizeddata['beds'] = (data.get('beds', '') - standards['beds']['mean']) / standards['beds']['std']
    standardizeddata['accomodates'] = (data.get('accomodates', '') - standards['accomodates']['mean']) / standards['accomodates']['std']

    return standardizeddata