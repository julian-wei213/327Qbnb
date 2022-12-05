from seleniumbase import BaseCase

from qbay_test.conftest import base_url

from qbay.models import Listing, User, db

from datetime import date

"""
This file defines all integration tests for the booking page.
"""


class FrontEndBookingTest(BaseCase):
    valid_name = "bookingname"
    valid_email = "booking@email.com"
    valid_password = 'Abc#123'
    valid_listing_title = ' house st'
    success_message = 'Listing Booked!'
    e_message = 'Invalid Input, Please Try Again!'
    counter = 0

    def test_1_booking(self, *_):
        '''
        A user can book a listing

        Testing method: partition testing
        '''
        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the registered user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # Create a Listing
        self.open(base_url + "/create_listing")
        self.type('#title', str(self.counter) + self.valid_listing_title)
        self.type('#description', "A little run down shack on the side street")
        self.type('#price', 500.00)

        self.click('input[type="submit"]')

        # open register page
        self.open(base_url + '/register')
        self.counter += 1

        # register a second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # add funds to second user's account
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 9999.00
        db.session.commit()
        # go to booking page
        self.open(base_url + "/booking")

        # book the listing other user posted
        listing = Listing.query.filter_by(
            title=str(self.counter - 1) + self.valid_listing_title).first()
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was sucessful
        self.assert_element('#message')
        self.assert_text(self.success_message, '#message')

        # try to book a listing not in the database
        listings = Listing.query.count()
        # use an id greater than amount of listings in database
        self.type('#l_id', listings + 1)
        start_date = date(2022, 12, 4)
        end_date = date(2024, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was unsucessful
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

    def test_2_booking(self, *_):
        '''
        A user cannot book a listing for his/her listing

        Testing method: partition testing
        '''
        # keep counter out of range of other tests
        self.counter = 50

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the registered user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # Create a Listing
        self.open(base_url + "/create_listing")
        self.type('#title', str(self.counter) + self.valid_listing_title)
        self.type('#description', "A little run down shack on the side street")
        self.type('#price', 500.00)

        self.click('input[type="submit"]')

        # add funds to user's account
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 9999.00
        db.session.commit()

        # go to booking page
        self.open(base_url + "/booking")

        # try to book listing user just posted
        listing = Listing.query.filter_by(
            title=str(self.counter) + self.valid_listing_title).first()
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was unsucessful
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # open register page
        self.open(base_url + '/register')
        self.counter += 1

        # register a second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # add funds to second user's account
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 9999.00
        db.session.commit()

        # go to booking page
        self.open(base_url + "/booking")

        # book the listing other user posted
        listing = Listing.query.filter_by(
            title=str(self.counter - 1) + self.valid_listing_title).first()
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was sucessful
        self.assert_element('#message')
        self.assert_text(self.success_message, '#message')

    def test_3_booking(self, *_):
        '''
        A user cannot book a listing that costs more than his/her balance

        Testing method: boundary testing
        '''
        # keep counter out of range of other tests
        self.counter = 100

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the registered user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # Create a Listing
        self.open(base_url + "/create_listing")
        self.type('#title', str(self.counter) + self.valid_listing_title)
        self.type('#description', "A little run down shack on the side street")
        self.type('#price', 500.00)

        self.click('input[type="submit"]')

        # open register page
        self.open(base_url + '/register')
        self.counter += 1

        # register a second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # sets funds to 1 cent below listing price
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 499.99
        db.session.commit()

        # go to booking page
        self.open(base_url + "/booking")

        # book the listing other user posted
        listing = Listing.query.filter_by(
            title=str(self.counter - 1) + self.valid_listing_title).first()
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was unsucessful
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # increase funds to exact price
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 500.00
        db.session.commit()

        # try to book again
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was sucessful
        self.assert_element('#message')
        self.assert_text(self.success_message, '#message')

    def test_4_booking(self, *_):
        '''
        A user cannot book a listing that is already booked with
        the overlapped dates

        Testing method: partition testing
        '''
        # keep counter out of range of other tests
        self.counter = 150

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the registered user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # Create a Listing
        self.open(base_url + "/create_listing")
        self.type('#title', str(self.counter) + self.valid_listing_title)
        self.type('#description', "A little run down shack on the side street")
        self.type('#price', 500.00)

        self.click('input[type="submit"]')

        # open register page
        self.open(base_url + '/register')
        self.counter += 1

        # register a second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the second user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # add funds to second user
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 1000.00
        db.session.commit()

        # go to booking page
        self.open(base_url + "/booking")

        # book the listing first user posted
        listing = Listing.query.filter_by(
            title=str(self.counter - 1) + self.valid_listing_title).first()
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 2, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was sucessful
        self.assert_element('#message')
        self.assert_text(self.success_message, '#message')

        # open register page
        self.open(base_url + '/register')
        self.counter += 1

        # register a third user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', str(self.counter) + self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # log in as the third user
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')

        # add funds to third user
        user = User.query.filter_by(
            email=str(self.counter) + self.valid_email).first()
        user.balance = 1000.00
        db.session.commit()

        # go to booking page
        self.open(base_url + "/booking")

        # try to book the listing first user posted as overlapping time
        self.type('#l_id', listing.id)
        start_date = date(2022, 12, 4)
        end_date = date(2023, 5, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was unsucessful
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # try to book the listing after second user's booking ends
        self.type('#l_id', listing.id)
        start_date = date(2023, 2, 3)
        end_date = date(2023, 3, 2)
        self.type('#start_date', str(start_date.year) +
                  str(start_date.month) + str(start_date.day))
        self.type('#end_date', str(end_date.year) +
                  str(end_date.month) + str(end_date.day))
        self.click('input[type="submit"]')

        # assert the booking was sucessful
        self.assert_element('#message')
        self.assert_text(self.success_message, '#message')

    def test_5_booking(self, *_):
        '''
        A booked listing will show up on the user's home page.

        To be implemented later...
        '''
