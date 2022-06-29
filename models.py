from routes import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON


class User(UserMixin, db.Model):
    """User of the site."""

    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def get_id(self):
        return self.uid

class Property(db.Model):
    """Properties owned by users."""

    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(512), nullable=False)
    HostResponseTime = db.Column(db.Integer, nullable=False)
    RoomType = db.Column(db.Integer, nullable=False)
    Beds = db.Column(db.Integer, nullable=False)
    Accommodates = db.Column(db.Integer, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    ReviewScore = db.Column(db.Float, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable = False)

class Listing(db.Model):
    """Listings from AirBnB Data"""

    __tablename__ = "listings_postgres_clone3"

    id = db.Column(db.Integer, primary_key=True)
    listing_url = db.Column(db.String(2048), nullable=True)
    scrape_id = db.Column(db.Integer, nullable=True)
    last_scraped = db.Column(db.String(512), nullable=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    neighborhood_overview = db.Column(db.String(512), nullable=True)
    picture_url = db.Column(db.String(2048), nullable=True)
    host_id = db.Column(db.Integer, nullable=True)
    host_url = db.Column(db.String(2048), nullable=True)
    host_name = db.Column(db.String(512), nullable=True)
    host_location = db.Column(db.String(512), nullable=True)
    host_about = db.Column(db.String(2048), nullable=True)
    host_response_rate = db.Column(db.Integer, nullable=True)
    host_acceptance_rate = db.Column(db.Integer, nullable=True)
    host_is_superhost = db.Column(db.String(1), nullable=True)
    host_thumbnail_url = db.Column(db.String(2048), nullable=True)
    host_picture_url = db.Column(db.String(2048), nullable=True)
    host_neighborhood = db.Column(db.String(512), nullable=True)
    host_listings_count = db.Column(db.Integer, nullable=True)
    host_total_listings_count = db.Column(db.Integer, nullable=True)
    host_verifications = db.Column(db.Integer, nullable=True)
    host_has_profile_pic = db.Column(db.String(1), nullable=True)
    host_identity_verified = db.Column(db.String(1), nullable=True)
    neighborhood = db.Column(db.String(512), nullable=True)
    neighborhood_cleansed = db.Column(db.String(512), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(128), nullable=True)
    room_type = db.Column(db.String(128), nullable=True)
    accommodates = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    bathrooms_text = db.Column(db.String(128), nullable=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    beds = db.Column(db.Integer, nullable=True)
    amenities = db.Column(db.String(2048), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    minimum_nights = db.Column(db.Integer, nullable=True)
    maximum_nights = db.Column(db.Integer, nullable=True)
    minimum_minimum_nights = db.Column(db.Integer, nullable=True)
    maximum_minimum_nights = db.Column(db.Integer, nullable=True)
    minimum_maximum_nights = db.Column(db.Integer, nullable=True)
    maximum_maximum_nights = db.Column(db.Integer, nullable=True)
    minimum_nights_avg_ntm = db.Column(db.Integer, nullable=True)
    maximum_nights_avg_ntm = db.Column(db.Integer, nullable=True)
    calendar_updated = db.Column(db.String(128), nullable=True)
    has_availability = db.Column(db.String(1), nullable=True)
    availability_30 = db.Column(db.Float, nullable=True)
    availability_60 = db.Column(db.Float, nullable=True)
    availability_90 = db.Column(db.Float, nullable=True)
    availability_365 = db.Column(db.Float, nullable=True)
    calendar_last_scraped = db.Column(db.String(128), nullable=True)
    number_of_reviews = db.Column(db.Integer, nullable=True)
    number_of_review_ltm = db.Column(db.Integer, nullable=True)
    number_of_reviews_l30d = db.Column(db.Integer, nullable=True)
    first_review = db.Column(db.String(128), nullable=True)
    review_scores_rating = db.Column(db.Float, nullable=True)
    review_scores_accuracy = db.Column(db.Float, nullable=True)
    review_scores_cleanliness = db.Column(db.Float, nullable=True)
    review_scores_checkin = db.Column(db.Float, nullable=True)
    review_scores_communication = db.Column(db.Float, nullable=True)
    review_scores_location = db.Column(db.Float, nullable=True)
    review_scores_value = db.Column(db.Float, nullable=True)
    license = db.Column(db.String(128), nullable=True)
    instant_bookable = db.Column(db.String(1), nullable=True)
    calculated_host_listings_count = db.Column(db.Integer, nullable=True)
    calculated_host_listings_count_entire_homes = db.Column(db.Integer, nullable=True)
    calculated_host_listings_count_private_rooms = db.Column(db.Integer, nullable=True)
    calculated_host_listings_count_shared_rooms = db.Column(db.Integer, nullable=True)
    reviews_per_month = db.Column(db.Float, nullable=True)
    host_number_of_years = db.Column(db.Float, nullable=True)
    host_response_time_a_few_days_or_more = db.Column(db.Integer, nullable=True)
    host_response_time_within_a_day = db.Column(db.Integer, nullable=True)
    host_response_time_within_a_few_hours = db.Column(db.Integer, nullable=True)
    host_response_time_within_an_hour = db.Column(db.Integer, nullable=True)
    closeness_to_landmark = db.Column(db.Float, nullable=True)
    closeness_to_subway = db.Column(db.Float, nullable=True)

class ReviewClone(db.Model):
    """Digest of relevant review data"""

    __tablename__ = "reviews_clone_fin"

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings_postgres_clone3.id'), nullable=False)
    date = db.Column(db.String(128), nullable=True)
    reviewer_id = db.Column(db.Integer, nullable=True)
    comments = db.Column(db.String(2048), nullable=True)
    polarity = db.Column(db.Float, nullable=True)
    subjectivity = db.Column(db.Float, nullable=True)
    reviewer_gender = db.Column(db.String(64), nullable=True)
    nouns = db.Column(db.String(512), nullable=True)
    adjectives = db.Column(db.String(512), nullable=True)
