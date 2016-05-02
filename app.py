from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.stormpath import StormpathManager, current_user

app = Flask(__name__)

# config
app.config.from_object('config')

db = SQLAlchemy(app)
stormpath_manager = StormpathManager(app)


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
    parking = db.Column(db.String(200))
    resort_fee = db.Column(db.String(20))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    def __init__(self, name="", url="", parking="", resort_fee="", location_id=""):
        self.name = name
        self.url = url
        self.parking = parking
        self.resort_fee = resort_fee
        self.location_id = location_id


# admin setup
class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user does not have access
        return redirect('/login')

admin = Admin(app, name='GovSwag Admin', template_mode='bootstrap3')
admin.add_view(MyModelView(Hotel, db.session))
admin.add_view(MyModelView(Location, db.session))

# Views
@app.route('/')
def index():
    locations = Location.query.all()
    return render_template('index.html', locations=locations)


@app.route('/<city_url_slug>')
def hotel_list(city_url_slug):
    location = Location.query.filter_by(city_url_slug=city_url_slug).first()
    hotels = location.hotels
    return render_template('hotels.html', location=location, hotels=hotels)


if __name__ == '__main__':
    app.run(debug=True)
