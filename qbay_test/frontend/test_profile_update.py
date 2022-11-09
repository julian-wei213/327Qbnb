from seleniumbase import BaseCase
import random
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import *

"""
This file defines all integration tests for the user profile update page

# TODO:
- update username (t/f)
- update email (t/f)
- update postal code (t/f)
- update addr (t/f)
- update all t no f
- update 3 t but 1 f


def test_r3_3_update_user():
    '''
      Testing R3-3: Postal code has to be a valid Canadian postal code.
      Follow style A1A 1A1
    '''
    # confirm works with valid canadian postal code
    user = register('userr33', 'anemailr33@email.com', valid_password)
    for i in range(100):
        new_postal_code = generate_canadian_postal_code()
        user.update_postal_code(new_postal_code)
        assert user.update_postal_code(new_postal_code) is True
        assert user.postal_code == new_postal_code
    # doesn't work with non-valid code
    new_postal_code = 'A1A A1A'
    user.update_postal_code(new_postal_code)
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code
    # example 2
    new_postal_code = 'A1A1A1'
    user.update_postal_code(new_postal_code)
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code


def generate_canadian_postal_code():
    '''
    Generates a random Canadian postal code
    '''
    code = ""
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += " "
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    return code


def test_r3_4_update_user():
    '''
      Testing R3-4: User name follows the requirements above.
    '''
    user = register('userr34', 'emailr34@email.com', valid_password)
    # Confirm valid username is acceptable
    new_name = "test namer34"
    assert user.update_name(new_name) is True
    assert user.username == new_name
    # User name has to be non-empty
    new_name = ""
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # alphanumeric-only
    new_name = 'asd#f12!3'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # space allowed only if it is not as the prefix or suffix.

    # space in prefix should fail
    new_name = ' asdf123'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # space in suffix should fail
    new_name = 'asdf123 '
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # longer than 2 characters and less than 20 characters.

    # less than 3 should fail
    new_name = '12'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # greater than 19 should fail
    new_name = ''.join(random.choice(string.ascii_letters) for i in range(20))
    print(new_name)
    assert user.update_name(new_name) is False
    assert user.username != new_name

"""

def helper_generate_valid_canadian_postal_code():
    '''
    Helper Function: Generates a random valid Canadian postal code
    '''
    code = ""
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += " "
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    return code

def helper_generate_invalid_canadian_postal_code():
    '''
    Helper Function: Generates a random invalid Canadian postal code
    '''
    str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+ []?><';:'"
    code = ""
    code += random.choice(str)
    code += random.choice(str)
    code += random.choice(str)
    code += " "
    code += random.choice(str)
    code += random.choice(str)
    code += random.choice(str)
    return code


class FrontEndProfileUpdateTest(BaseCase):

    def test_r3_1_profile_update(self, *_):
        '''
        Testing R3-1: A user is only able to update his/her user name,
         user email, billing address, and postal code.

        Testing Method: Input Partitioning
        '''

        # Custom messages
        e_msg = 'Invalid Input, Please Try Again!'
        s_msg = 'Profile Updated!'

        tmp_email = 'tmp.user@yahoo.com'
        tmp_pass = 'tmp!USER123'
        tmp_name = 'User'

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', tmp_email)
        self.type('#name', tmp_name)
        self.type('#password', tmp_pass)
        self.type('#password2', tmp_pass)
        self.click('input[type="submit"]')

        # login
        self.type('#email', tmp_email)
        self.type('#password', tmp_pass)
        self.click('input[type="submit"]')

        # open profile_update page
        self.open(base_url + '/profile_update')

        # Case 1: valid name
        self.type('#name', 'new' + tmp_name)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case 2: valid email
        self.type('#email', 'new' + tmp_email)
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case 3: valid address
        self.type('#bill_addr', 'new address')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case 4: valid postal
        self.type('#postal_code', 'B2B 2B2')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case 5: invalid name; valid email, address, postal
        self.type('#name', ' invalid' + tmp_name) # Invalid Name
        self.type('#email', 'new' + tmp_email)
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2B 2B2')

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 6: invalid email; valid name, address, postal
        self.type('#name', 'new' + tmp_name)
        self.type('#email', ' invalid' + tmp_email) # Invalid Email
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2B 2B2')

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 7: invalid address; valid name, email, postal
        # There is no restriction for address, it can be literally anything (not testable)

        # Case 8: invalid postal; valid name, email, address
        self.type('#name', 'new' + tmp_name)
        self.type('#email', ' invalid' + tmp_email)
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2? 2B2') # Invalid Email

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 9: valid name, email, address, postal
        self.type('#name', 'new' + tmp_name)
        self.type('#email', 'new' + tmp_email)
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2B 2B2')

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')


    def test_r3_2_profile_update(self, *_):
        '''
        Testing R3-2: Postal code should be non-empty, alphanumeric-only,
        and no special characters such as !.

        Testing Method: Input Partitioning
        '''

        # Custom messages
        e_msg = 'Invalid Input, Please Try Again!'
        s_msg = 'Profile Updated!'

        tmp_email = 'tmp.user@yahoo.com'
        tmp_pass = 'tmp!USER123'
        tmp_name = 'User'

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', tmp_email)
        self.type('#name', tmp_name)
        self.type('#password', tmp_pass)
        self.type('#password2', tmp_pass)
        self.click('input[type="submit"]')

        # login
        self.type('#email', tmp_email)
        self.type('#password', tmp_pass)
        self.click('input[type="submit"]')

        # open profile_update page
        self.open(base_url + '/profile_update')

        # Case 1: Non-Empty
        self.type('#postal_code', ' ')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 2: AlphaNum Only
        self.type('#postal_code', 'A1A #B1')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 3: Valid Postal Code
        self.type('#postal_code', 'A1A 1B1')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')


    def test_r3_3_profile_update(self, *_):
        '''
        Testing R3-3: Postal code has to be a valid Canadian postal code.
        Follow style A1A 1A1

        Testing Method: Shotgun Testing
        '''

        # Custom messages
        e_msg = 'Invalid Input, Please Try Again!'
        s_msg = 'Profile Updated!'

        tmp_email = 'tmp1.user@yahoo.com'
        tmp_pass = 'tmp1!USER123'
        tmp_name = 'User1'

        # open register page
        self.open(base_url + '/register')

        # register
        self.type('#email', tmp_email)
        self.type('#name', tmp_name)
        self.type('#password', tmp_pass)
        self.type('#password2', tmp_pass)
        self.click('input[type="submit"]')

        # login
        self.type('#email', tmp_email)
        self.type('#password', tmp_pass)
        self.click('input[type="submit"]')

        # open profile_update page
        self.open(base_url + '/profile_update')

        # Shotgun test: valid input
        for i in range(10):
            s_code = helper_generate_valid_canadian_postal_code()
            self.type('#postal_code', s_code)
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text(s_msg, '#message')

        # Shotgun test: invalid input
        for i in range(10):
            e_code = helper_generate_invalid_canadian_postal_code()
            self.type('#postal_code', e_code)
            self.click('input[type="submit"]')
            self.assert_element('#message')
            self.assert_text(e_msg, '#message')


    # def test_r3_4_profile_update(self, *_):
    #     '''
    #     Testing R3-3: Postal code has to be a valid Canadian postal code.
    #     Follow style A1A 1A1
    #
    #     Testing Method: Shotgun Testing
    #     '''
