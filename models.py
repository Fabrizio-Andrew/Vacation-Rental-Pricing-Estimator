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
    host_response_rate = db.Column(db.Integer, nullable=True)
    host_is_superhost = db.Column(db.String(1), nullable=True)
    neighbourhood_cleansed = db.Column(db.String(512), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(128), nullable=True)
    room_type = db.Column(db.String(128), nullable=True)
    accommodates = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    beds = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    host_number_of_years = db.Column(db.Float, nullable=True)
    host_response_time_a_few_days_or_more = db.Column(db.Integer, nullable=True)
    host_response_time_within_a_day = db.Column(db.Integer, nullable=True)
    host_response_time_within_a_few_hours = db.Column(db.Integer, nullable=True)
    host_response_time_within_an_hour = db.Column(db.Integer, nullable=True)
    closeness_to_landmark = db.Column(db.Float, nullable=True)
    closeness_to_subway = db.Column(db.Float, nullable=True)
    review_scores_rating = db.Column(db.Float, nullable=True)

class ReviewClone(db.Model):
    """Digest of relevant review data"""

    __tablename__ = "reviews_clone_fin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(128), nullable=True)
    reviewer_id = db.Column(db.Integer, nullable=True)
    reviewer_name = db.Column(db.String(128), nullable=True)
    comments = db.Column(db.String(2048), nullable=True)
    polarity = db.Column(db.Float, nullable=True)
    subjectivity = db.Column(db.Float, nullable=True)
    reviewer_gender = db.Column(db.String(64), nullable=True)
    nouns = db.Column(db.String(512), nullable=True)
    adjectives = db.Column(db.String(512), nullable=True)
