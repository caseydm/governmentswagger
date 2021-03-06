from flask import Flask, render_template, redirect, request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.stormpath import StormpathManager, current_user, login_required
from models import db, Hotel, Location, Image
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug import secure_filename
from flask_wtf.file import FileField
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
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
    hotels = ''
    location = Location.query.filter_by(city_url_slug=city_url_slug).first()
    if location:
        hotels = location.hotels
    return render_template('hotel_list.html', location=location, hotels=hotels)


def hotel_query():
    return Hotel.query


class ImageForm(Form):
    name = StringField('Name')
    file = FileField('Your image')
    cover_image = BooleanField('Cover Image')
    hotel = QuerySelectField(query_factory=hotel_query, get_label='name', allow_blank=True)


# upload image and list images
@app.route('/admin/images', methods=['GET', 'POST'])
@login_required
def admin_images():
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
        cover_image = form.cover_image.data
        key = filename
        image = Image(name, url, key, cover_image, hotel.id)
        db.session.add(image)
        db.session.commit()
        return redirect('/admin/images')
    else:
        hotels = Hotel.query.all()
    return render_template('admin/images.html', form=form, hotels=hotels)


# delete image
@app.route('/admin/images/delete/<image_id>', methods=['GET'])
@login_required
def admin_delete_image(image_id):
    # get image object from db
    image = Image.query.filter_by(id=image_id).first_or_404()

    # delete from S3
    s3 = boto3.resource('s3')
    obj = s3.Object('governmentswagger', image.key)
    obj.delete()

    # delete from db
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted from database and S3', 'success')
    return redirect('/admin/images')


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
