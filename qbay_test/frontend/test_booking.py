from seleniumbase import BaseCase

from qbay_test.conftest import base_url

"""
This file defines all integration tests for the booking page.
"""


class FrontEndBookingTest(BaseCase):


    def test_1_booking(self, *_):
        '''
        A user can book a listing

        Testing method: partition testing
        '''


    def test_2_booking(self, *_):
        '''
        A user cannot book a listing for his/her listing

        Testing method: partition testing
        '''

    def test_3_booking(self, *_):
        '''
        A user cannot book a listing that costs more than his/her balance

        Testing method: boundary testing
        '''
    
    def test_4_booking(self, *_):
        '''
        A user cannot book a listing that is already booked with
        the overlapped dates

        Testing method: partition testing
        '''

    def test_5_booking(self, *_):
        '''
        A booked listing will show up on the user's home page

        Testing method: 
        '''


