from flask import Flask
from flask_sqlalchemy import SQLAlchemy

// setting up SQLAlchemy and data models so we can map data models into database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Rating(db.Model):
    """Data model for Rating

    Properties:
    - id (Integer)
    - stars (Numeric)
    """
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        """Returns the string representation of Rating"""
        return '<Rating %r>' % self.stars
