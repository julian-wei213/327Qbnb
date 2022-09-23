from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# setting up SQLAlchemy and data models so we can map into db tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Transaction(db.Model):
    """Data model for Transactions
    Attributes
    ----------
    id : Integer
        represents a unique id
    listing_id : Integer
        represents the id of associated listing in database
    user_id : Integer
        represents the id of user in database that booked the listing
    """
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Returns the string representation of Transaction"""
        return '<%r booking %r>' % \
            (Listing.query.filter_by(id=self.listing_id),
                User.query.filter_by(id=self.user_id))
