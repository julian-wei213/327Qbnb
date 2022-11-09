from seleniumbase import BaseCase
# from selenium.webdriver.common.by import By
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
"""

def register_test_user(self):
    """
    Comment
    """
    self.open(base_url + '/register')
    self.type("#email", "user1@gmail.com")
    self.type("#name", "user1")
    self.type("#password", "123456")
    self.type("#password2", "123456")
    self.click('input[type="submit"]')


def login_test_session(self):
    """
    Comment
    """
    self.open(base_url + '/login')
    self.type("#email", "user1@gmail.com")
    self.type("#password", "123456")
    self.click('input[type="submit"]')


class UserUpdatePageTest(BaseCase):
    """
    Comment
    """

    def test_username_update_success(self, *_):
        """
        Comment
        """
        register_test_user(self)
        login_test_session(self)

        self.open(base_url + '')
        # self.assert_element('#update_profile')
        # self.assert_text('auth', '#auth')

        # self.open(base_url + 'profile_update')
        # self.type("#name", "validusername")
        # self.click('input[type="submit"]')
        # self.assert_element("#message")
        # self.assert_text("Profile Updated!", "#message")

    # def test_login_success(self, *_):
    #     """
    #     This is a sample front end unit test to login to home page
    #     and verify if the tickets are correctly listed.
    #     """
    #     # open login page
    #     self.open(base_url + '/login')
    #     # fill email and password
    #     self.type("#email", "test0@test.com")
    #     self.type("#password", "123456")
    #     # click enter button
    #     self.click('input[type="submit"]')
    #
    #     # after clicking on the browser (the line above)
    #     # the front-end code is activated
    #     # and tries to call get_user function.
    #     # The get_user function is supposed to read data from database
    #     # and return the value. However, here we only want to test the
    #     # front-end, without running the backend logics.
    #     # so we patch the backend to return a specific user instance,
    #     # rather than running that program. (see @ annotations above)
    #
    #     # open home page
    #     self.open(base_url)
    #     # test if the page loads correctly
    #     # self.assert_element("#welcome-header")
    #     # self.assert_text("Welcome u0 !", "#welcome-header")
    #     # other available APIs
