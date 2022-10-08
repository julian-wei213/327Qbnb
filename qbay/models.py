from queue import Empty
from sre_parse import SPECIAL_CHARS
from qbay import app
from flask_sqlalchemy import SQLAlchemy


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(
        db.String(80), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False,
        primary_key=True)
    password = db.Column(
        db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


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
    # check if email or password are empty
    if not email or not password:
        return False
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False
    # check if password is at least 6 characters, with upper, lower and special characters
    if not (len(password) >= 6 and check_str_contains_lower(password) and check_str_contains_upper(password) and check_str_contains_special(password)):
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True

def check_str_contains_upper(str):
    for x in str:
        if x == x.upper():
            return True
    return False

def check_str_contains_lower(str):
    for x in str:
        if x == x.lower():
            return True
    return False

def check_str_contains_special(str):
    return any(special in str for special in SPECIAL_CHARS)

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
