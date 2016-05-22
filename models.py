from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Models
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    city_url_slug = db.Column(db.String(80), unique=True, nullable=False)
    hotels = db.relationship('Hotel', backref='location', lazy='dynamic')

    def __repr__(self):
        return self.city


class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text())
    govt_rate_offered = db.Column(db.Boolean())
    url = db.Column(db.String(80))
    reservation_url = db.Column(db.String(80))
    free_parking = db.Column(db.Boolean())
    self_parking = db.Column(db.Boolean())
    self_parking_cost = db.Column(db.Numeric(10, 2))
    valet_parking = db.Column(db.Boolean())
    valet_parking_cost = db.Column(db.Numeric(10, 2))
    resort_fee = db.Column(db.Boolean())
    resort_fee_cost = db.Column(db.Numeric(10, 2))
    free_wifi = db.Column(db.Boolean())
    wifi_cost = db.Column(db.Numeric(10, 2))
    star_rating = db.Column(db.Integer())
    address = db.Column(db.String(300))
    phone = db.Column(db.String(30))
    trip_advisor_rank = db.Column(db.Integer())
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    images = db.relationship('Image', backref='hotel', lazy='dynamic')


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(250), nullable=False)
    key = db.Column(db.String(200), nullable=False)
    cover_image = db.Column(db.Boolean())
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    def __init__(self, name, url, key, hotel_id):
        self.name = name
        self.url = url
        self.key = key
        self.hotel_id = hotel_id
