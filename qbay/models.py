from qbay import app
from flask_sqlalchemy import SQLAlchemy
from datetime import date


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True)
    username = db.Column(
        db.String(80), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False)
    password = db.Column(
        db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Listing(db.Model):
    '''
    Listing model
      Attributes:
        id (Integer):              listing id
        title (String):            listing title
        description (String):      listing description
        price (Decimal):           listing price
        last_modified_date (Date): last modified date of listing
        owner_id (Integer):        listing owner's id
    '''
    id = db.Column(
        db.Integer, primary_key=True)
    title = db.Column(
        db.String(80), unique=True, nullable=False)
    description = db.Column(
        db.String(2000), nullable=False)
    price = db.Column(
        db.Float(2, True), nullable=False)
    last_modified_date = db.Column(
        db.Date)
    owner_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Listing %r>' % self.title


# create all tables
db.create_all()


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]


def create_listing(title: str, description: str, price: float,
                   last_modified_date: date, owner_id: int):
    '''
    Creates a listing
      Attributes:
        title (str):               listing title
        description (str):         listing description
        price (float):             listing price
        last_modified_date (date): last modified date of listing
        owner_id (int):            listing owner's id
      Returns:
        The listing object if succeeded otherwise None
    '''
    # Satisfy R4-1
    if title == '':
        return None
    
    if title[0] == ' ' or title[-1] == ' ':
        return None
    
    if not title.replace(' ', '').isalnum():
        return None

    # Satisfy R4-2
    if len(title) > 80:
        return None
    
    # Satisfy R4-3
    if len(description) < 20 or len(description) > 2000:
        return None
    
    # Satisfy R4-4
    if len(description) <= len(title):
        return None
    
    # Satisfy R4-5
    if price < 10 or price > 10000:
        return None
    
    # Satisfy R4-6
    if last_modified_date <= date(2021, 1, 2) or \
       last_modified_date >= date(2025, 1, 2):
        return None
    
    # Satisfy R4-7
    user = User.query.filter_by(id=owner_id).first()
    if user is None:
        return None
    
    if user.email == '':
        return None
    
    # Satisfy R4-8
    if len(Listing.query.filter_by(title=title).all()) > 0:
        return None
    
    # create a new listing
    listing = Listing(title=title, description=description,
                      price=price, last_modified_date=last_modified_date,
                      owner_id=owner_id)
    
    # add it to the current database session
    db.session.add(listing)
    # actually save the user object
    db.session.commit()

    return listing