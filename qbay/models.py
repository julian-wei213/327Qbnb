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

    def update_name(name):
        '''
        A user is able to update his/her user name.
        '''

    def update_email(email):
        '''
        A user is able to update his/her user email.
        '''

    def update_address(address):
        '''
        A user is able to update his/her billing address.
        '''

    def update_postal_code(postal_code):
        '''
        A user is able to update his/her postal code.
        '''


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


def is_postal_code(code):
    '''
    Returns true if the string 'code' is a valid Canadian postal code, and false
    if not.

    Canadian Postal Code has the format:
    A1A A1A
    '''
    # Check that the string contains exactly 7 characters, otherwise return false
    # as the string cannot be a valid postal code.
    if (len(code) != 7):
        return False

    # Check that the 1st character in the string is a letter, return false if not
    if (not code[0].isalpha()):
        return False

    # Check that the 2nd character in the string is a digit, return false if not
    if (not code[1] in "0123456789"):
        return False

    # Check that the 3rd character in the string is a letter, return false if not
    if (not code[2].isalpha()):
        return False

    # Check that the 4th character in the string is a space, return false if not
    if (code[3] != " "):
        return False

    # Check that the 5th character in the string is a digit, return false if not
    if (not code[4] in "0123456789"):
        return False

    # Check that the 6th character in the string is a letter, return false if not
    if (not code[5].isalpha()):
        return False

    # Check that the 7th character in the string is a digit, return false if not
    if (not code[6] in "0123456789"):
        return False

    return True
