import random
import string
import re
from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from qbay.models import check_str_contains_lower, \
    check_str_contains_special, check_str_contains_upper

"""
This file defines all integration tests for the frontend homepage.
"""


def generate_string(string_length):
    """
    Helper method that generates a random string of string_length
    """
    generated = ""
    for i in range(string_length):
        # pick an upper or lower case character
        letters = string.ascii_letters
        rng = random.randint(0, 10)
        # 10% of the time, pick a special character instead
        if rng == 9:
            letters = string.punctuation
        # another 10% of time, pick whitespace instead
        elif rng == 8:
            letters = ' '
        # another 10% of time, pick numbers instead
        elif rng == 7:
            letters = string.digits
        generated += (random.choice(letters))
    return generated


class FrontEndRegistrationTest(BaseCase):
    valid_name = "username"
    invalid_name = '--coolKid#1--'
    valid_email = "x@email.com"
    invalid_email = "eMaIl"
    valid_password = 'Abc#123'
    invalid_password = 'asdfghjkl'
    login_page_message = 'Please login'
    passwords_not_matching_message = 'The passwords do not match'
    e_message = 'Registration failed.'
    counter = 0

    def test_r1_1_user_register(self, *_):
        '''
        Testing R1-1: Email/Password cannot be empty

        Testing method: input partitioning
        '''
        # open register page
        self.open(base_url + '/register')

        # register with empty email and empty password
        self.type('#email', " ")
        self.type('#name', self.valid_name)
        self.type('#password', " ")
        self.type('#password2', " ")
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # register with empty email, valid password
        self.type('#email', " ")
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # register with empty password, valid email
        self.type('#email', self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', ' ')
        self.type('#password2', ' ')
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # register with valid email and valid password
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')

    def test_r1_2_user_register(self, *_):
        '''
        Testing R1-2: A user is uniquely identified by their id

        Testing method: Can't be tested in frontend
        '''

    def test_r1_3_user_register(self, *_):
        '''
        Testing R1-2: Email follows addr-spec defined by RFC 5322

        Testing method: output partitioning
        '''
        # selenium uses multiple instances of class to run tests
        # have to preserve counter from previous tests
        self.counter = 150
        # open register page
        self.open(base_url + '/register')
        # First register with an invalid email to show submiting fails
        self.type('#email', self.invalid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # register with valid email to get successful output
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')

        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')

    def test_r1_4_user_register(self, *_):
        '''
        Testing R1-4: Password has to meet the required complexity:
        minimum length 6, at least one upper case, at least one lower case,
        and at least one special character.

        Testing method: shotgun testing
        '''
        # selenium uses multiple instances of class to run tests
        # have to preserve counter from previous tests
        self.counter = 300
        # open register page
        self.open(base_url + '/register')
        # attempt 100 different passwords
        for i in range(100):
            string_length = random.randint(4, 10)
            test_string = generate_string(string_length)
            # if password is valid
            if (len(test_string) >= 6 and check_str_contains_lower(test_string)
                and check_str_contains_upper(test_string)
                    and check_str_contains_special(test_string)):
                self.counter += 1
                self.type('#email', str(self.counter) + self.valid_email)
                self.type('#name', self.valid_name)
                self.type('#password', test_string)
                self.type('#password2', test_string)
                self.click('input[type="submit"]')
                # assert we are now at the login page
                self.assert_element('#message')
                self.assert_text(self.login_page_message, '#message')
                # return to register page for next test
                self.open(base_url + '/register')
            # if password wasn't valid
            else:
                self.counter += 1
                self.type('#email', str(self.counter) + self.valid_email)
                self.type('#name', self.valid_name)
                self.type('#password', test_string)
                self.type('#password2', test_string)
                self.click('input[type="submit"]')
                # assert user gets an error message
                self.assert_element('#message')
                self.assert_text(self.e_message, '#message')

    def test_r1_5_user_register(self, *_):
        '''
        Testing R1-5: Username has to be non-empty, alpahnumerical,
        and space allowed only as non prefix/suffix

        Testing method: Shotgun testing
        '''
        # selenium uses multiple instances of class to run tests
        # have to preserve counter from previous tests
        self.counter = 500
        # open register page
        self.open(base_url + '/register')
        # attempt 100 different usernames
        for i in range(100):
            string_length = random.randint(3, 9)
            test_string = generate_string(string_length)

            # if username is valid
            name_validation = re.compile('^(?! )[A-Za-z0-9 ]*(?<! )$')
            if re.fullmatch(name_validation, test_string):
                self.counter += 1
                self.type('#email', str(self.counter) + self.valid_email)
                self.type('#name', test_string)
                self.type('#password', self.valid_password)
                self.type('#password2', self.valid_password)
                self.click('input[type="submit"]')
                # assert we are now at the login page
                self.assert_element('#message')
                self.assert_text(self.login_page_message, '#message')
                # return to register page for next test
                self.open(base_url + '/register')
            # if password wasn't valid
            else:
                self.counter += 1
                self.type('#email', str(self.counter) + self.valid_email)
                self.type('#name', test_string)
                self.type('#password', self.valid_password)
                self.type('#password2', self.valid_password)
                self.click('input[type="submit"]')
                # assert user gets an error message
                self.assert_element('#message')
                self.assert_text(self.e_message, '#message')

    def test_r1_6_user_register(self, *_):
        '''
        Testing R1-6: Username has to be more than 2 character and less than 20

        Testing method: input boundary testing
        '''
        # selenium uses multiple instances of class to run tests
        # have to preserve counter from previous tests
        self.counter = 700
        # open register page
        self.open(base_url + '/register')
        # 3 character username
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', 'a' * 3)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')
        # return to register page for next test
        self.open(base_url + '/register')

        # 2 character username
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', 'a' * 2)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # username 19 characters
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', 'a' * 19)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')
        # return to register page for next test
        self.open(base_url + '/register')

        # username 20 characters
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', 'a' * 20)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

    def test_r1_7_user_register(self, *_):
        '''
        Testing R1-7: If the email has been used, the operation failed.

        Testing method: input partitioning
        '''
        # selenium uses multiple instances of class to run tests
        # have to preserve counter from previous tests
        self.counter = 900
        # open register page
        self.open(base_url + '/register')
        # register first user
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')
        # return to register page for next test
        self.open(base_url + '/register')

        # try to register second user with same email
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert user gets an error message
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # prove it works if they just change email
        self.counter += 1
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')

    def test_r1_8_user_register(self, *_):
        '''
        Testing R1-8: Shipping Address is empty at the time of registration

        Testing method: can't be tested in frontend
        '''

    def test_r1_9_user_register(self, *_):
        '''
        Testing R1-9: Postal Code is empty at the time of registration

        Testing method: can't be tested in frontend
        '''

    def test_r1_10_user_register(self, *_):
        '''
        Testing R1-10: Balance should be initialized as 100

        Testing method: can't be tested in frontend
        '''
