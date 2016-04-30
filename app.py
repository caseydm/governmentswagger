import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.stormpath import StormpathManager, current_user

app = Flask(__name__)

# config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['STORMPATH_API_KEY_ID'] = os.environ.get('STORMPATH_API_KEY_ID')
app.config['STORMPATH_API_KEY_SECRET'] = os.environ.get('STORMPATH_API_KEY_SECRET')
app.config['STORMPATH_APPLICATION'] = os.environ.get('STORMPATH_APPLICATION')

db = SQLAlchemy(app)
stormpath_manager = StormpathManager(app)


# Models
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True)

    def __init__(self, city=""):
        self.city = city

    def __repr__(self):
        return self.city


class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(80))
    parking = db.Column(db.String(200))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    city = db.relationship(Location, backref='Hotel')

    def __init__(self, name="", url="", parking="", location_id=""):
        self.name = name
        self.url = url
        self.parking = parking
        self.location_id = location_id

db.create_all()

# admin setup
class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/login')

admin = Admin(app, name='GovSwag Admin', template_mode='bootstrap3')
admin.add_view(MyModelView(Hotel, db.session))
admin.add_view(MyModelView(Location, db.session))


# Views
@app.route('/')
def index():
    hotels = Hotel.query.all()
    return render_template('index.html', hotels=hotels)

if __name__ == '__main__':
    app.run(debug=True)
