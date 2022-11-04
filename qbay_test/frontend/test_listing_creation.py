from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User

import random

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndCreateListingTest(BaseCase):
    
    def test_r4_1_create_listing(self, *_):
        '''
        Testing R4-1: The title of the product has to be alphanumeric-only, and
        space allowed only if it is not as prefix and suffix.
        
        Testing method: Input partitioning
        '''
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/register')
        
        # register
        self.type('#email', testing_email)
        self.type('#name', testing_name)
        self.type('#password', testing_password)
        self.type('#password2', testing_password)
        self.click('input[type="submit"]')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')
        
        # Case 1: Alpha-only
        self.type('#title', 'TheTitle')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 2: Num-only
        self.type('#title', '000000000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 3: Alphanum-only
        self.type('#title', 'Title00000000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 4: Alpha-only with middle space
        self.type('#title', 'TheT itle')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 5: Num-only with middle space
        self.type('#title', '00000 000000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 6: Alphanum-only with middle space
        self.type('#title', 'Title000 00000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 7: Alpha-only with prefix space
        self.type('#title', ' TheTitle')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')
        
        # Case 8: Num-only with prefix space
        self.type('#title', ' 000000000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')
        
        # Case 9: Alphanum-only with prefix space
        self.type('#title', ' Title00000000')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')
        
        # Case 10: Alpha-only with postfix space
        self.type('#title', 'TheTitle ')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')
        
        # Case 11: Num-only with postfix space
        self.type('#title', '000000000 ')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')
        
        # Case 12: Alphanum-only with postfix space
        self.type('#title', 'Title00000000 ')
        self.type('#description', 'description of listing')
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', '#message')

    def test_r4_2_create_listing(self, *_):
        '''
        Testing R4-2: The title of the product is no longer than 80 characters.
        
        Testing method: Input boundary testing
        ''' 
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Case 1: Title is 80 characters
        self.type('#title', '0' * 80)
        self.type('#description', 'description of listing' + '0' * 80)
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 2: Title is 81 characters
        self.type('#title', '0' * 81)
        self.type('#description', 'description of listing' + '0' * 81)
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', 'h4')
        
    def test_r4_3_create_listing(self, *_):
        '''
        Testing R4-3: The description of the product can be arbitrary
        characters, with a minimum length of 20 characters and a maximum
        of 2000 characters.
        
        Testing method: Shotgun testing
        '''
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Shotgun test: Legal set
        for i in range(10):
            self.type('#title', '43test1' + str(i))
            self.type('#description', '0' * random.randint(20, 2000))
            self.type('#price', 30.00)
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('Listing Creation succeeded!', '#message')
            
        # Shotgun test: Illegal set; < 20 chars
        for i in range(10):
            self.type('#title', '43test2' + str(i))
            self.type('#description', '0' * random.randint(1, 19))
            self.type('#price', 30.00)
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('Listing Creation failed.', 'h4')
            
        # Shotgun test: Illegal set; > 2000 chars
        for i in range(5):
            self.type('#title', '43test2' + str(i))
            self.type('#description', '0' * random.randint(2001, 2050))
            self.type('#price', 30.00)
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('Listing Creation failed.', 'h4')
        
    def test_r4_4_create_listing(self, *_):
        '''
        Testing R4-4: Description has to be longer than the product's title.
        
        Testing method: Input boundary testing
        '''
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Case 1: Description is longer than title by 1 character
        self.type('#title', 'h' * 20)
        self.type('#description', '0' * 21)
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 2: Description is equal to title length
        self.type('#title', 'j' * 20)
        self.type('#description', '0' * 20)
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', 'h4')
        
    def test_r4_5_create_listing(self, *_):
        '''
        Testing R4-5: Price has to be of range [10, 10000].
        
        Testing method: Input boundary testing
        '''
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Case 1: Price is $10.00
        self.type('#title', '45test1')
        self.type('#description', '0' * 20)
        self.type('#price', 10.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 2: Price is $9.99
        self.type('#title', '45test2')
        self.type('#description', '0' * 20)
        self.type('#price', 9.99)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('9.99', '#price')
        
        # Case 3: Price is $10000.00
        self.type('#title', '45test3')
        self.type('#description', '0' * 20)
        self.type('#price', 10000.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
        # Case 4: Price is $10000.01
        self.type('#title', '45test4')
        self.type('#description', '0' * 20)
        self.type('#price', 10000.01)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('10000.01', '#price')
        
    def test_r4_6_create_listing(self, *_):
        '''
        Testing R4-6: last_modified_date must be after 2021-01-02
        and before 2025-01-02.
        
        Testing method: Shotgun testing
        '''
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')
        
        # Shotgun test
        for i in range(10):
            self.type('#title', '46test' + str(i))
            self.type('#description', '0' * random.randint(20, 200))
            self.type('#price', round(random.random() + 10.00, 2))
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text('Listing Creation succeeded!', '#message')

    def test_r4_7_create_listing(self, *_):
        '''
        Testing R4-7: owner_email cannot be empty. The owner of the
        corresponding product must exist in the database.
        
        Testing method: Cannot test
        '''
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Case 4: Price is $10000.01
        self.type('#title', '47test')
        self.type('#description', '0' * 20)
        self.type('#price', 30.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
        
    def test_r4_8_create_listing(self, *_):
        '''
        Testing R4-8: A user cannot create products that have the same title.
        
        Testing method: Input partitioning
        '''
        
        testing_email = 'testcreatelisting@hotmail.com'
        testing_password = 'abcDEF123!'
        testing_name = 'Testing Man'
        
        # open register page
        self.open(base_url + '/login')

        # login
        self.type('#email', testing_email)
        self.type('#password', testing_password)
        self.click('input[type="submit"]')
        
        # open create_listing page
        self.open(base_url + '/create_listing')

        # Init create listing
        self.type('#title', '48test')
        self.type('#description', '0' * 20)
        self.type('#price', 10.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')

        # Case 1: Listing has same title
        self.type('#title', '48test')
        self.type('#description', '0' * 20)
        self.type('#price', 10.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation failed.', 'h4')
        
        # Case 2: Listing has differnt title
        self.type('#title', '48testdiff')
        self.type('#description', '0' * 20)
        self.type('#price', 10.00)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text('Listing Creation succeeded!', '#message')
