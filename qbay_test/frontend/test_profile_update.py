from seleniumbase import BaseCase
import random
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import *

"""
This file defines all integration tests for the user profile update page
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
    str = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklm"
           "nopqrstuvwxyz1234567890!@#$%^&*()_+[]?><';:'")
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
        self.type('#name', ' invalid' + tmp_name)  # Invalid Name
        self.type('#email', 'new' + tmp_email)
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2B 2B2')

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 6: invalid email; valid name, address, postal
        self.type('#name', 'new' + tmp_name)
        self.type('#email', ' invalid' + tmp_email)  # Invalid Email
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2B 2B2')

        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case 7: invalid address; valid name, email, postal
        # There is no restriction for address, it can
        # be literally anything (not testable)

        # Case 8: invalid postal; valid name, email, address
        self.type('#name', 'new' + tmp_name)
        self.type('#email', ' invalid' + tmp_email)
        self.type('#bill_addr', 'new address')
        self.type('#postal_code', 'B2? 2B2')  # Invalid Email

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

    def test_r3_4_profile_update(self, *_):
        '''
        Testing R3-4: User name follows the requirements above.
            R1-5: User name has to be non-empty, alphanumeric-only, and space
                allowed only if it is not as the prefix or suffix.
            R1-6: User name has to be longer than 2 characters and less than
                20 characters.

        Testing Method: Input Partitioning
        '''

        # Custom messages
        e_msg = 'Invalid Input, Please Try Again!'
        s_msg = 'Profile Updated!'

        tmp_email = 'tmp2.user@yahoo.com'
        tmp_pass = 'tmp2!USER123'
        tmp_name = 'User2'

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

        # Case1: Non-Empty
        self.type('#name', ' ')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case2: Alpha-Only
        self.type('#name', 'ABCabc')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case3: Num-Only
        self.type('#name', '123456')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case4: AlphaNum-Only
        self.type('#name', 'ABCabc123')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case5: Alpha-Only with Middle Space
        self.type('#name', 'ABC abc')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case6: Num-Only with Middle Space
        self.type('#name', '123 456')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case7: AlphaNum-Only with Middle Space
        self.type('#name', 'ABC 123 abc')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case8: Alpha-Only with Prefix Space
        self.type('#name', ' ABCabc')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case9: Num-Only with Prefix Space
        self.type('#name', ' 123456')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case10: AlphaNum-Only with Prefix Space
        self.type('#name', ' ABC123abc')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case11: Alpha-Only with Suffix Space
        self.type('#name', 'ABCabc ')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case12: Num-Only with Suffix Space
        self.type('#name', '123456 ')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case13: AlphaNum-Only with Suffix Space
        self.type('#name', 'ABC123abc ')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case14: Less than 2 characters
        self.type('#name', 'a')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case15: 2 characters
        self.type('#name', 'a1')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case16: more than 2 characters less than 20
        self.type('#name', 'ABCDab cd1234')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(s_msg, '#message')

        # Case16: 20 characters
        self.type('#name', 'ABCDEFGabcdefg 12345')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')

        # Case17: more than 20
        self.type('#name', 'ABCDEFGabcdefg 123456789')
        self.click('input[type="submit"]')
        self.assert_element('#message')
        self.assert_text(e_msg, '#message')
