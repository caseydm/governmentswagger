from flask import Flask, render_template, redirect, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.stormpath import StormpathManager, current_user, login_required
from models import db, Hotel, Location, Image
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug import secure_filename
from flask_wtf.file import FileField
from flask_wtf import Form
from wtforms import StringField, SelectField
import boto3


# app setup
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
stormpath_manager = StormpathManager(app)


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


class ImageForm(Form):
    name = StringField('Name')
    file = FileField('Your image')
    hotel = SelectField('Hotel', choices=[('3', 'St Croix'), ('4', 'Sheraton')])


# upload image and list images
@app.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload():
    form = ImageForm()
    if form.validate_on_submit():

        # save file to S3
        s3 = boto3.client('s3')
        file = request.files[form.file.name]
        filename = secure_filename(file.filename)
        s3.put_object(Body=file, Bucket='governmentswagger', Key=filename)

        # save image info to database
        url = 'http://s3.amazonaws.com/governmentswagger/' + filename
        name = form.name.data
        hotel = form.hotel.data
        image = Image(name, url, hotel)
        db.session.add(image)
        db.session.commit()
        return redirect('/upload')
    else:
        hotels = Hotel.query.all()
    return render_template('upload.html', form=form, hotels=hotels)


# delete image
@app.route('/upload/delete/<image_id>', methods=['GET'])
#@login_required
def delete_image(image_id):
    image = Image.query.filter_by(id=image_id).first_or_404()

    db.session.delete(image)
    db.session.commit()
    return redirect('/upload')


# db migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


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
    manager.run()
