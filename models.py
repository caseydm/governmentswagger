from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Models
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True)
    city_url_slug = db.Column(db.String(80), unique=True)
    hotels = db.relationship('Hotel', backref='location', lazy='dynamic')

    def __init__(self, city="", city_url_slug=""):
        self.city = city
        self.city_url_slug = city_url_slug

    def __repr__(self):
        return self.city


class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(80))
    free_parking = db.Boolean()
    parking = db.Column(db.String(200))
    resort_fee = db.Column(db.String(20))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    def __init__(self, name="", url="", parking="", resort_fee="", location_id="", free_parking=""):
        self.name = name
        self.url = url
        self.parking = parking
        self.resort_fee = resort_fee
        self.location_id = location_id
        self.free_parking = free_parking
