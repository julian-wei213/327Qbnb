from seleniumbase import BaseCase

from qbay_test.conftest import base_url

"""
This file defines all integration tests for the login page.
"""


class FrontEndRegistrationTest(BaseCase):
    valid_name = "username"
    valid_email = "x@email.com"
    invalid_email = "eMaIl"
    valid_password = 'Abc#123'
    invalid_password = 'asdfghjkl'
    login_page_message = 'Please login'
    home_page_message = 'Welcome !'
    e_message = 'login failed'
    counter = 0

    def test_r2_1_login(self, *_):
        '''
        Testing R2-1: A user can log in using her/his email address
        and the password.

        Testing method: output partition testing
        '''
        # open register page
        self.open(base_url + '/register')

        # register with valid email and password
        self.type('#email', self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')

        # try to log in as a random user
        self.type('#email', 'different@email.com')
        self.type('#password', 'Cba#321')
        self.click('input[type="submit"]')
        # assert we were unable to login
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # try to log in as the registered user
        self.type('#email', self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')
        # assert we were able to login
        self.assert_element('#welcome-header')
        self.assert_text(self.home_page_message, '#welcome-header')

    def test_r2_2_login(self, *_):
        '''
        The login function should check if the supplied inputs meet the same
        email/password requirements as for registration, before checking the
        database.

        I recommend checking models.py to confirm that it doesn't bother
        querrying if requirements aren't met, but will still show that it at
        least doesn't succeed in logging in.

        Testing method: can't really test, but some input partition testing
                        because why not
        '''

        # open register page
        self.open(base_url + '/register')
        # register with valid email and password
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#name', self.valid_name)
        self.type('#password', self.valid_password)
        self.type('#password2', self.valid_password)
        self.click('input[type="submit"]')
        # assert we are now at the login page
        self.assert_element('#message')
        self.assert_text(self.login_page_message, '#message')

        # Confirm R1-1
        # try log in with empty password
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', ' ')
        self.click('input[type="submit"]')
        # assert we were unable to login
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # try log in with empty email
        self.type('#email', ' ')
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')
        # assert we were unable to login
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # Confirm R1-3
        # Login can't work with invalid email
        self.type('#email', self.invalid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')
        # assert we were unable to login
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # Confirm R1-4
        # Login can't work with invalid password
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.invalid_password)
        self.click('input[type="submit"]')
        # assert we were unable to login
        self.assert_element('#message')
        self.assert_text(self.e_message, '#message')

        # Confirm it does work if you use correct email/password
        self.type('#email', str(self.counter) + self.valid_email)
        self.type('#password', self.valid_password)
        self.click('input[type="submit"]')
        # assert we were able to login
        self.assert_element('#welcome-header')
        self.assert_text(self.home_page_message, '#welcome-header')
