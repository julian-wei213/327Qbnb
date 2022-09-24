from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# setting up SQLAlchemy and data models so we can map into db tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Listing(db.Model):
    """
    Listing class

    Attributes:
    ----------
    id : int
        primary key for the data table
    address : str
        string representing address of the listing, cannot be null
    price : float
        float representing the cost of the listing per night, cannot be null
    owner : int
        integer representing the id of the owner in the User table
    """

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # Return a str representing the id of the Listing class
        return '<Listing %r>' % self.id

class User(db.Model):
    """
    User data model

    Attributes
    ----------
    id : int
        integer representing the primary key
    name : str
        string representing a name, must not be null
    email : str
        string representing an email, must be unique and not be null
    password : str
        string representing user password, must not be null
    balance : float
        Float representing user bank balance, must not be null (default = 0)
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0)

    def __repr__(self):
        """Returns a string representing the class object"""
        return '<User %r>' % self.email


class Rating(db.Model):
    """Data model for Rating

    Attributes
    ----------
    id : Integer
        represents a unique id
    stars : Numeric
        represents the star rating
    """
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        """Returns the string representation of Rating"""
        return '<Rating %r>' % self.stars
