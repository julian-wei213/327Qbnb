import re
import random
from qbay import app
from flask_sqlalchemy import SQLAlchemy


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(80), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False)
    password = db.Column(
        db.String(120), nullable=False)
    ship_addr = db.Column(
        db.String(120), nullable=False)
    postal_code = db.Column(
        db.String(120), nullable=False)
    balance = db.Column(
        db.Float, nullable=False, default=0)

    def __repr__(self):
        return '<ID %r>' % self.id


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
        The object User otherwise None
    '''

    # R1-1 check if the email is empty
    if len(email) <= 0:
        return None

    # R1-2 each user is identified by a unique id
    # User.id is a primary_key and automatically generates a
    # new unique id for each new User

    # R1-3 The email has to follow addr-spec defined in RFC 5322
    email_val = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')
    if not re.fullmatch(email_val, email):
        return None

    # R1-4 Password has to meet the required complexity

    # R1-5 Username has to be non-empty
    if name == '':
        return None

    # R1-5 Alpahnumerical, and space allowed only as not prefix/suffix
    name_validation = re.compile('^(?! )[A-Za-z0-9 ]*(?<! )$')
    if not re.fullmatch(name_validation, name):
        return None

    # R1-6 Username has to be longer than 2 but shorter than 20
    if len(name) < 3:
        return None
    elif len(name) > 19:
        return None

    # R1-7 check if the email has been used:
    existing_email = User.query.filter_by(email=email).all()
    if len(existing_email) > 0:
        return None

    # R1-8 Shipping Adress is empty at the time of registration
    # Initialize User with ship_addr as ''

    # R1-9 Postal code is empty at the time of registration
    # Initialize User with postal_code as ''

    # R1-10 Balance should be initialized as 100
    balance = 100

    # create a new user
    user = User(username=name, email=email, password=password,
                ship_addr='', postal_code='', balance=balance)

    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return user


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
