import re
import string
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
        db.String(120), nullable=False, default='')
    postal_code = db.Column(
        db.String(120), nullable=False, default='')
    balance = db.Column(
        db.Float, nullable=False, default=100)

    def __repr__(self):
        return '<ID %r>' % self.id

    def update_name(self, name):
        '''
        A user is able to update his/her user name.
        '''
        # R1-5 Username has to be non-empty
        if name == '':
            return False

        # R1-5 Alpahnumerical, and space allowed only as not prefix/suffix
        name_validation = re.compile('^(?! )[A-Za-z0-9 ]*(?<! )$')
        if not re.fullmatch(name_validation, name):
            return False

        # R1-6 Username has to be longer than 2 but shorter than 20
        if len(name) < 3:
            return False
        elif len(name) > 19:
            return False
        
        self.username = name 
        return True

    def update_email(self, email):
        '''
        A user is able to update his/her user email.
        '''
        # R1-1 check if the email is empty
        if not email:
            return False
        # R1-3 The email has to follow addr-spec defined in RFC 5322
        email_val = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_val, email):
            return False
        
        self.email = email
        return True

    def update_address(self, address):
        '''
        A user is able to update his/her billing address.
        '''
        self.ship_addr = address
    
    def update_postal_code(self, postal_code):
        '''
        A user is able to update his/her postal code.
        '''
        canadian_postal_code = re.compile('[A-Z][0-9][A-Z] [0-9][A-Z][0-9]')
        if not re.fullmatch(canadian_postal_code, postal_code):
            return False

        self.postal_code = postal_code
        return True


# create all tables
db.create_all()


def register(name: str, email: str, password: str):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        The object User otherwise None
    '''

    # R1-1 check if the email or password are empty
    if not email or not password:
        return None

    # ensure password is a string
    password = str(password)

    # R1-2 each user is identified by a unique id
    # User.id is a primary_key and automatically generates a
    # new unique id for each new User

    # R1-3 The email has to follow addr-spec defined in RFC 5322
    email_val = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')
    if not re.fullmatch(email_val, email):
        return None

    # R1-4 Password has to meet the required complexity
    # check if password is at least 6 characters,
    # with upper, lower and special characters
    if not (len(password) >= 6
            and check_str_contains_lower(password)
            and check_str_contains_upper(password)
            and check_str_contains_special(password)):
        return None

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
    # Default is set to 100 in the User class

    # create a new user
    user = User(username=name, email=email, password=password)

    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return user


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
    return any(special in str for special in string.punctuation)


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