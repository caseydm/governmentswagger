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
    url = db.Column(db.String(80))
    free_parking = db.Column(db.Boolean())
    self_parking = db.Column(db.Boolean())
    valet_parking = db.Column(db.Boolean())
    self_parking_cost = db.Column(db.String(200))
    valet_parking_cost = db.Column(db.String(200))
    resort_fee = db.Column(db.Boolean())
    resort_fee_cost = db.Column(db.String(20))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
