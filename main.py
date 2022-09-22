from flask import Flask
from flask_sqlalchemy import SQLAlchemy

// setting up SQLAlchemy and data models so we can map data models into database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=true)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    owner = db.Column(db.Integer)

    def __repr__(self):
        return '<Listing %r>' % self.id

    def get_address(self):
        return '<Listing %r>' % self.address

    def get_price(self):
        return '<Listing %r>' % self.price

    def get_owner(self):
        return '<Listing %r>' % self.owner
