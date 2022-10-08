from sre_parse import SPECIAL_CHARS
from qbay.models import *
import string

def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u0', 'test0@test.com', '123456') is True
    assert register('u0', 'test1@test.com', '123456') is True
    assert register('u1', 'test0@test.com', '123456') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 1234567)
    assert user is None

def test_r3_1_update_user():
    '''
      Testing R3-1: A user is only able to update his/her user name, user email, billing address, and postal code.
    '''
    user = login('test0@test.com', 123456)
    new_name = "new " + user.username
    new_email = "new" + user.email
    new_address = "new" + user.address
    new_postal_code = user.postal_code
    # for new postal code, just increment second digit by 1
    new_postal_code[0] = (new_postal_code[1] + 1) % 10
    user_update_name(new_name)
    user_update_email(new_address, new_postal_code)
    user_update_address(new_address)
    user_update_postal_code(new_postal_code)
    assert user.username == new_name
    assert user.email == new_email
    assert user.address == new_address
    assert user.postal_code == new_postal_code
    


def test_r3_2_update_user():
    '''
      Testing R3-2: Postal code should be non-empty, alphanumeric-only, and no special characters such as !.
    '''
    for user in User:
      # not empty
      assert user.postal_code
      # alphanumeric only
      assert all(char in (string.ascii_letters + string.digits + " ") for char in user.postal_code)
      # no special characters
      assert not any(char in SPECIAL_CHARS for char in user.postal_code)


def test_r3_3_update_user():
    '''
      Testing R3-3: Postal code has to be a valid Canadian postal code.
      Follow style A1A 1A1
    '''
    for user in User:
      assert is_postal_code(user.postal_code)
    


def test_r3_4_update_user():
    '''
      Testing R3-4: User name follows the requirements above.
    '''

