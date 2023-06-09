import re
import string
from qbay import app
from flask_sqlalchemy import SQLAlchemy
from datetime import date


'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


class User(db.Model):
    '''
    User model
      Attributes:
        id (Integer):              user id
        username (String):         username
        email (String):            user email
        password (String):         user password
        ship_addr (String):        user ship address
        postal_code (String):      user postal code
        balance (Integer):         user balance
    '''
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

    def update_user(self, username: str = None, email: str = None,
                    ship_addr: str = None, postal_code: str = None):
        '''
        Updates user properties.
        '''
        ut = et = st = pt = True
        if username:
            ut = self.update_name(username)
        if email:
            et = self.update_email(email)
        if ship_addr:
            st = self.update_address(ship_addr)
        if postal_code:
            pt = self.update_postal_code(postal_code)

        if ut and et and st and pt:
            return True
        else:
            return False

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
        db.session.commit()
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
        db.session.commit()
        return True

    def update_address(self, address):
        '''
        A user is able to update his/her billing address.
        '''
        self.ship_addr = address
        db.session.commit()
        return True

    def update_postal_code(self, postal_code):
        '''
        A user is able to update his/her postal code.
        '''
        canadian_postal_code = re.compile('[A-Z][0-9][A-Z] [0-9][A-Z][0-9]')
        if not re.fullmatch(canadian_postal_code, postal_code):
            return False

        self.postal_code = postal_code
        db.session.commit()
        return True


class Review(db.Model):
    '''
    Listing model
      Attributes:
        id (Integer):              listing id
        user_id (Integer):         id of reviewer
        listing_id (Integer):      id of listing
        review text (String):      review text
        date (Date):               date of the review
    '''
    id = db.Column(
        db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(
        db.Integer, db.ForeignKey('listing.id'), nullable=False)
    review_text = db.Column(
        db.String(2000), nullable=False)
    date = db.Column(
        db.Date)

    def __repr__(self):
        return '<Listing %r>' % self.title


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


class Booking(db.Model):
    '''
    Booking model
      Attributes:
        id (Integer):              booking id
        user_id (Integer):         user id
        listing_id (Integer)       listing id
        booking_date (Date)        date of booking
        start_date (Date)          start date of stay
        end_date (Date)            end date of stay
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'),
                           nullable=False)
    booking_date = db.Column(db.Date, default=date.today())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Booking %r>' % self.id
    
    
def create_booking(user_id: int, listing_id: int, 
                   start_date: date, end_date: date):
    '''
    Creates a booking
      Attributes:
        user_id (int)          user id
        listing_id (int):      listing id
        start_date (date):     start date of stay
        end_date (date):       end date of stay
      Returns:
        The booking object if succeeded otherwise None
    '''

    # Check types
    if not isinstance(user_id, int):
        return None
    
    if not isinstance(listing_id, int):
        return None
    
    if not isinstance(start_date, date):
        return None
    
    if not isinstance(end_date, date):
        return None
    
    # start_date must be before end_date
    if start_date > end_date:
        return None
    
    listing = Listing.query.filter_by(id=listing_id).first()
    
    # listing does not exist
    if listing is None:
        return None
    
    # cannot book for user's own listing
    if user_id == listing.owner_id:
        return None
    
    user = User.query.filter_by(id=user_id).first()
    
    # user does not exist
    if user is None:
        return None
    
    # user is too poor
    if listing.price > user.balance:
        return None
    
    bookings = Booking.query.filter_by(listing_id=listing_id).all()
    
    # check for date overlaps
    for book in bookings:
        if start_date >= book.start_date and \
           start_date <= book.end_date:
            return None
        
        if end_date >= book.start_date and \
           end_date <= book.end_date:
            return None
    
    # create booking object
    booking = Booking(user_id=user_id, listing_id=listing_id, 
                      booking_date=date.today(), start_date=start_date,
                      end_date=end_date)
    
    # add it to the current database session
    db.session.add(booking)
    # actually save the user object
    db.session.commit()

    return booking
    

# create all tables
db.create_all()


def update_listing(listing, title=None, description=None, price=None):
    '''
    Updates a listing
      Attributes:
        listing (Listing)          Listing object
        title (str):               listing title (optional)
        description (str):         listing description (optional)
        price (float):             listing price (optional)
      Returns:
        The listing object if succeeded otherwise None
    '''

    # If all three optional arguments are skipped
    if title is None and description is None and price is None:
        return None

    # If listing is not of instance Listing
    if not isinstance(listing, Listing):
        return None

    # If title was given
    if title is not None:

        # If title is of instance str
        if not isinstance(title, str):
            return None

        # If title is a empty str
        if title == "":
            return None

        # Satisfy R4-2
        if len(title) > 80:
            return None

        # Satisfy R4-1
        check = re.match("^(?! )[A-Za-z0-9 ]*(?<! )$", title)

        if check is None:
            return None

        # Satisfy R4-8
        existed = Listing.query.filter_by(title=title,
                                          owner_id=listing.owner_id).all()
        if len(existed) > 0 and listing.title != title:
            return None

        # Update title
        listing.title = title

    # If description was given
    if description is not None:

        # If description is of instance str
        if not isinstance(description, str):
            return None

        # Satisfy R4-3
        if len(description) < 20 or len(description) > 2000:
            return None

        # If new title was given or not
        if title is not None:

            # Satisfy R4-4
            if len(description) <= len(title):
                return None
        else:

            # Satisfy R4-4
            if len(description) <= len(listing.title):
                return None

        # Update description
        listing.description = description

    # If price was given
    if price is not None:

        # If price is of instane float
        if not isinstance(price, float):
            return None

        # Satisfy R4-5
        if price < 10 or price > 10000:
            return None

        # Satisfy R5-2
        if price <= listing.price:
            return None

        # Update price
        listing.price = price

    # Satisfy R4-6 and R5-3
    if date.today() > date(2021, 1, 2) and \
       date.today() < date(2025, 1, 2):
        listing.last_modified_date = date.today()
    else:
        return None

    # Commit updates
    db.session.commit()

    # Return listing
    return listing


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
    if isinstance(price, float) or isinstance(price, int):
        if price < 10 or price > 10000:
            return None
    else:
        return None

    # Satisfy R4-6
    if isinstance(last_modified_date, date):
        if last_modified_date <= date(2021, 1, 2) or \
           last_modified_date >= date(2025, 1, 2):
            return None
    else:
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

    # R1-1 check if the email or password are empty
    if not email or not password:
        return None

    # ensure password is a string
    password = str(password)

    # R1-2 each user is identified by a unique id
    # User.id is a primary_key and automatically generates a
    # new unique id for each new User

    # R1-3 The email has to follow addr-spec defined in RFC 5322
    # initial simple check
    if ("@" not in email):
        return None
    # thorough check
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
    '''
    Checks if str contains an upper case letter
    '''
    for x in str:
        if x == x.upper():
            return True
    return False


def check_str_contains_lower(str):
    '''
    Checks if str contains a lower case letter
    '''
    for x in str:
        if x == x.lower():
            return True
    return False


def check_str_contains_special(str):
    '''
    Checks if str contains punctuations
    '''
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
    # R2-2 The login function should check if the supplied inputs
    # meet the same email/password requirements as above(R1-1, R1-3, R1-4),
    # before checking the database.

    # R1-1 check if the email or password are empty
    if not email or not password:
        return None
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

    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None

    return valids[0]
