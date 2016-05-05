from flask import Flask, render_template, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.stormpath import StormpathManager, current_user
from models import db, Hotel, Location
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# app setup
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
stormpath_manager = StormpathManager(app)

# db migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# views
@app.route('/')
def index():
    locations = Location.query.all()
    return render_template('index.html', locations=locations)


@app.route('/<city_url_slug>')
def hotel_list(city_url_slug):
    location = Location.query.filter_by(city_url_slug=city_url_slug).first()
    hotels = location.hotels
    return render_template('hotels.html', location=location, hotels=hotels)


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

if __name__ == '__main__':
    manager.run(debug=True)
