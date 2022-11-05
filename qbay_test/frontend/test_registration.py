from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
import random

"""
This file defines all integration tests for the frontend homepage.
"""


# class FrontEndHomePageTest(BaseCase):

#     def test_login_success(self, *_):
#         """
#         This is a sample front end unit test to login to home page
#         and verify if the tickets are correctly listed.
#         """
#         # open login page
#         self.open(base_url + '/login')
#         # fill email and password
#         self.type("#email", "test0@test.com")
#         self.type("#password", "123456")
#         # click enter button
#         self.click('input[type="submit"]')

#         # after clicking on the browser (the line above)
#         # the front-end code is activated
#         # and tries to call get_user function.
#         # The get_user function is supposed to read data from database
#         # and return the value. However, here we only want to test the
#         # front-end, without running the backend logics.
#         # so we patch the backend to return a specific user instance,
#         # rather than running that program. (see @ annotations above)

#         # open home page
#         self.open(base_url)
#         # test if the page loads correctly
#         # self.assert_element("#welcome-header")
#         # self.assert_text("Welcome u0 !", "#welcome-header")
#         # other available APIs


class FrontEndUpdateListingTesting(BaseCase):

    def test_r5_1_update_listing(self, *_):
        """
        R5-1: One can update all attributes of the listing,
        except owner_id and last_modified_date

        modified from create_listing code

        testing method: input partitioning
        """

        # Set up testing info
        default_email = "updatelisting@email.com"
        default_password = "Password22$"
        default_name = "John Doe"

        # Register
        self.open(base_url + '/register')

        self.type('#email', default_email)
        self.type('#name', default_name)
        self.type('#password', default_password)
        self.type('#password2', default_password)

        self.click('input[type="submit"]')

        # Login
        self.type('#email', default_email)
        self.type('#password', default_password)

        self.click('input[type="submit"]')

        # Create some Listings
        self.open(base_url + "/create_listing")

        self.type('#title', "209 Test St")
        self.type('#description', "A little run down shack on the side street")
        self.type('#price', 500.00)

        self.click('input[type="submit"]')

        self.type('#title', "200 Test St")
        self.type('#description', "A very big mansion on the main street")
        self.type('#price', 5000.00)

        self.click('input[type="submit"]')

        # Listings page
        self.open(base_url + "/listing")
        self.find_partial_link_text("Update").click()

        # R5-1: One can update all attributes of the listing,
        # except owner_id and last_modified_date.

        # Update title only
        self.type('#title', "209 Test Street")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update title only fail
        self.type('#title', "200 Test St")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update description only
        self.type('#description', "Sorry about the place, \
                    it is a little run down but CHEEAP!")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update description only fail
        self.type('#description', "smo")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update title and price only
        self.type('#title', "209 Test St renovated")
        self.type('#price', 600.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update title, price fail 
        self.type('#title', "209 Test St renovated twice!!")
        self.type('#price', 20.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update title fail, price
        self.type('#title', "200 Test St")
        self.type('#price', 600.05)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update title fail, price fail
        self.type('#title', "200 Test St")
        self.type('#price', 50)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update descrption and price only
        self.type('#description', "The newly renovated place is the \
                    best for your buck!!")
        self.type('#price', 601.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update descrption fail and price only
        self.type('#description', "smo")
        self.type('#price', 602.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update descrption and price fail only
        self.type('#description', "The newly renovated place is the best \
                    for your buck!! AC!")
        self.type('#price', 50.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update descrption fail and price fail only
        self.type('#description', "smo")
        self.type('#price', 50.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update price only
        self.type('#price', 602.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update price only fail
        self.type('#price', 602.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Update title, description and price
        self.type('#title', "209 Test St renovated with AC")
        self.type('#description', "The newly renovated place is the best for \
                  your buck!! It also has AC")
        self.type('#price', 603.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Update title fail, description fail and price fail
        self.type('#title', "200 Test St")
        self.type('#description', "smo")
        self.type('#price', 50.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

    def test_r5_2_update_listing(self, *_):
        """
        R5-2: Price can be only increased but cannot be decreased :)

        tesing method: input boundary 
        """

        # Set up testing info
        default_email = "updatelisting@email.com"
        default_password = "Password22$"

        # Login
        self.open(base_url + '/login')
        self.type('#email', default_email)
        self.type('#password', default_password)

        self.click('input[type="submit"]')

        # Listings page
        self.open(base_url + "/listing")
        self.find_partial_link_text("Update").click()

        # Check highest fail case
        self.type('#price', 602.99)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Check lowest fail case
        self.type('#price', 10.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Check equals fail case
        self.type('#price', 603.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Check lowest success case
        self.type('#price', 603.01)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Check highest success case
        self.type('#price', 10000)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

    def test_r5_3_update_listing(self, *_):
        """
        R5-3: last_modified_date should be updated when the update operation
        is successful.

        testing method: no available tests as date is in month/day,
        also unable to assign date at creation, must wait a whole
        day to see date changed
        """

        # Set up testing info
        default_email = "updatelisting@email.com"
        default_password = "Password22$"

        # Login
        self.open(base_url + '/login')
        self.type('#email', default_email)
        self.type('#password', default_password)

        self.click('input[type="submit"]')

        # Listings page
        self.open(base_url + "/listing")
        self.find_partial_link_text("Update").click()

    def test_r5_4_update_listing(self, *_):
        """
        R5-4: When updating an attribute, one has to make sure that it follows
        the same requirements as above.

        testing method: shotgun, input partitioning, and boundary testing
        """
        # Set up testing info
        default_email = "updatelisting@email.com"
        default_password = "Password22$"

        # Login
        self.open(base_url + '/login')
        self.type('#email', default_email)
        self.type('#password', default_password)

        self.click('input[type="submit"]')

        # Listings page
        self.open(base_url + "/listing")
        self.find_partial_link_text("Update").click()

        # R4-1: partitioning testing

        # Case 1: Alpha-only
        self.type('#title', "GrooveStreet")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 2: Num-only
        self.type('#title', '289109299')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 3: Alphanum-only
        self.type('#title', '309Street')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 4: Alpha-only with middle space
        self.type('#title', 'third Street')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 5: Num-only with middle space
        self.type('#title', '28901 3218')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 6: Alphanum-only with middle space
        self.type('#title', '309th Street')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 7: Alpha-only with prefix space
        self.type('#title', ' SecondStreet')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Case 8: Num-only with prefix space
        self.type('#title', ' 3211092')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Case 9: Alphanum-only with prefix space
        self.type('#title', ' Street5920th')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Case 10: Alpha-only with postfix space
        self.type('#title', 'Streetfirst ')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Case 11: Num-only with postfix space
        self.type('#title', '31293100 ')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Case 12: Alphanum-only with postfix space
        self.type('#title', 'Street9210 ')
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # R4-2: boundary testing

        # Case 1: Title is 80 characters
        self.type('#title', 'f' * 80)
        self.type('#description', 'description of listing' + 'x' * 80)
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Case 2: Title is 81 characters
        self.type('#title', 'f' * 81)
        self.type('#description', 'description of listing' + 'x' * 81)
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # R4-3: shotgun testing

        # Shotgun test: Legal set
        for i in range(10):
            self.type('#title', '999th Str' + str(i))
            self.type('#description', 'x' * random.randint(20, 2000))
            self.type('#price', '')
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('List Update PASSED', '#message')

        # Shotgun test: Illegal set; < 20 chars
        for i in range(10):
            self.type('#title', '999th Str' + str(i))
            self.type('#description', 'x' * random.randint(1, 19))
            self.type('#price', '')
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('List Update FAILED', '#message')

        # Shotgun test: Illegal set; > 2000 chars
        for i in range(5):
            self.type('#title', '999th Str' + str(i))
            self.type('#description', 'x' * random.randint(2001, 2050))
            self.type('#price', '')
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('List Update FAILED', '#message')

        # R5-4: boundary testing

        # Title longer than description
        self.type("#title", 'f' * 21)
        self.type("#description", 'x' * 20)
        self.type("#price", '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Title shorter than description
        self.type("#title", 'f' * 19)
        self.type("#description", 'x' * 20)
        self.type("#price", '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')

        # Title equals description
        self.type("#title", 'f' * 20)
        self.type("#description", 'x' * 20)
        self.type("#price", '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # R5-4: boundary testing

        # Price below lower bound
        self.type("#price", 9.99)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # Price above upper bound
        self.type("#price", 10001)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # R6-4: Cannot test like R5-3

        # R7-4: Not relevant to update as can't change owner_id

        # R8-4: partition testing

        # There is a listing with title already
        self.type('#title', "200 Test St")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update FAILED', '#message')

        # There is no listing with title
        self.type('#title', "682 Test St")
        self.type('#price', '')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('List Update PASSED', '#message')
