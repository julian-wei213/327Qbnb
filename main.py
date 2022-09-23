from flask import Flask
from flask_sqlalchemy import SQLAlchemy

// setting up SQLAlchemy and data models so we can map data models into database tables
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
    address = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # Return a str representing the id of the Listing class
        return '<Listing %r>' % self.id
