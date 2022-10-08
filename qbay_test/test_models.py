from sre_parse import SPECIAL_CHARS
from qbay.models import *
import string
import random

def test_r1_1_user_register():
    '''
    Testing R1-1: Email cannot be empty. password cannot be empty.
    '''
    # empty email
    assert register('u0', '', '123456') is False
    # empty password
    assert register('u0', 'test0@test.com', '') is False


def test_r1_4_user_register():
    '''
    Testing R1-4: Password has to meet the required complexity: 
    minimum length 6, at least one upper case, at least one lower case, 
    and at least one special character.
    '''
    for i in range(100):
      string_length = random.randint(4, 10)
      test_string = generate_string(string_length)

      if (len(test_string) >= 6 and check_str_contains_lower(test_string) and check_str_contains_upper(test_string) and check_str_contains_special(test_string)):
        assert register('u_r1_4{i}', 'r1_4_%i@test.com'%(i), test_string) is True
      else:
        assert register('u_r1_4{i}', 'r1_4_%i@test.com'%(i), test_string) is False



def generate_string(string_length):
    generated = ""
    for i in range(string_length):
      # pick an upper or lower case character
      letters = string.ascii_letters
      rng = random.randint(0, 10)
      # 10% of the time, pick a special character instead
      if rng >= 9:
        letters = SPECIAL_CHARS
      generated += (random.choice(letters))
    return generated


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


def test_r2_2_login():
    '''
      Testing R2-2: The login function should check if the supplied inputs 
      meet the same email/password requirements as above, before checking the database.
    '''


def test_r3_1_update_user():
    '''
      Testing R3-1: A user is only able to update his/her user name, user email, billing address, and postal code.
    '''
    user = login('test0@test.com', 123456)
    old_name = user.username
    old_email = user.email
    old_address = user.address
    old_postal_code = user.postal_code
    new_name = "new " + user.username
    new_email = "new" + user.email
    new_address = "new" + user.address
    new_postal_code = "new" + user.postal_code
    update_user(new_name, new_email, new_address, new_postal_code)
    assert user.username == new_name
    assert user.email == new_email
    assert user.address == new_address
    assert user.postal_code == new_postal_code
    


def test_r3_2_update_user():
    '''
      Testing R3-2: Postal code should be non-empty, alphanumeric-only, and no special characters such as !.
    '''
    for i in range(100):
      string_length = random.randint(0, 10)
      test_string = generate_string(string_length)

      if (test_string and not check_str_contains_special(test_string)):
        assert update_user("name", "email", "address", test_string) is True
      else:
        assert update_user("name", "email", "address", test_string) is False
    

def test_r3_3_update_user():
    '''
      Testing R3-3: Postal code has to be a valid Canadian postal code.
      Follow style: A1A 1A1
    '''
    


def test_r3_4_update_user():
    '''
      Testing R3-4: User name follows the requirements above.
    '''
