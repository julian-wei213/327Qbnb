from qbay.models import register, login

valid_password = 'abc#123'

def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    '''
    # show that login works
    user_registered = register('userr21', 'anemailr21@email.com', valid_password)
    user_log = login('anemailr21@email.com', valid_password)
    assert user_log is not None
    assert user_log == user_registered

def test_r2_2_login():
    '''
    The login function should check if the supplied inputs meet the same email/password requirements as above, before checking the database.
    '''
    # This can't really be tested here, just go check models.py to confirm that it doesn't bother querrying if requirements aren't met