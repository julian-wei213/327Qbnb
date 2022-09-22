from flask import Flask
from flask_sqlalchemy import SQLAlchemy

// setting up SQLAlchemy and data models so we can map data models into database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Numeric)

    def __repr__(self):
        return '<Rating %r>' % self.stars
