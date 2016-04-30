import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


# Models
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    city = db.Column(db.String(80))
    url = db.Column(db.String(80))

    def __init__(self, name, city, url):
        self.name = name
        self.city = city
        self.url = url

db.create_all()

# admin setup
admin = Admin(app, name='Hotels', template_mode='bootstrap3')
admin.add_view(ModelView(Hotel, db.session))


# Views
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
