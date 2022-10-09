from sre_parse import SPECIAL_CHARS
from qbay.models import register, login, check_str_contains_lower, check_str_contains_upper, check_str_contains_special
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


def test_r1_1_user_register():
    '''
    Testing R1-1: Email/Password cannot be empty
    '''
    # First assess that normal case works
    assert register('user1', '0@email.com', 123456) is not None
    # Second ensure an empty email would fail
    assert register('user2', '', 123456) is None


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by their id
    '''
    # First assess that two new users are valid
    user1 = register('user3', '3@email.com', 123456)
    assert user1 is not None
    user2 = register('user4', '4@email.com', 123456)
    assert user2 is not None
    # Second make sure their id's are unique
    assert user1.id != user2.id


def test_r1_3_user_register():
    '''
    Testing R1-2: Email follows addr-spec defined by RFC 5322
    '''
    # First assess that the an email is valid given the constraints
    assert register('us2', 'an.eMa_il@gmail.uk.ca.com', 123456) is not None
    # Second test cases that must fail
    assert register('us2', 'im proper@gmail.com', 123456) is None
    assert register('us2', 'improper@gmail..com', 123456) is None
    assert register('us2', '.improper@gmail.com', 123456) is None
    assert register('us2', 'improper@@gmail.com', 123456) is None
    assert register('us2', 'improper@gmail.', 123456) is None
    assert register('us2', 'improper@.com', 123456) is None
    assert register('us2', '_improper@.com', 123456) is None
    assert register('us2', 'i@mproper@.com', 123456) is None


def test_r1_4_user_register():
    '''
    Testing R1-4: Password has to meet the required complexity
    '''


def test_r1_5_user_register():
    '''
    Testing R1-5: Username has to be non-empty, alpahnumerical,
    and space allowed only as prefix/suffix
    '''
    # First assess that a username is valid based on the constraints
    assert register('u U0', 'anemail1@gmail.com', 123456) is not None
    # Second test cases that need to fail
    assert register(' uU0', 'anemail2@gmail.com', 123456) is None
    assert register('uU0 ', 'anemail3@gmail.com', 123456) is None
    assert register('', 'anemail4@gmail.com', 123456) is None


def test_r1_6_user_register():
    '''
    Testing R1-6: Username has to be more than 2 character and less than 20
    '''
    # First assess that the username is valid if within the constraint
    assert register('use', 'anemail6@gmail.com', 123456) is not None
    assert register(
        'uabcdefghijklmnop12', 'anemail8@gmail.com', 123456) is not None
    # Second assess that username is not valid if outside of constraint
    assert register('u', 'anemail5@gmail.com', 123456) is None
    assert register('us', 'anemail6@gmail.com', 123456) is None
    assert register(
        'uabcdefghijklmnop123', 'anemail7@gmail.com', 123456) is None


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''
    # First create two usernames with two
    # different emails and that the operation is valid
    assert register('us0', 'test0@test.com', '123456') is not None
    assert register('us0', 'test1@test.com', '123456') is not None
    # Second attempt to make a new user with an already
    # used email and ensure its not valid
    assert register('us1', 'test0@test.com', '123456') is None


def test_r1_8_user_register():
    '''
    Testing R1-8: Shipping Address is empty at the time of registration
    '''
    # First assess that a newly registered user is valid
    user = register('user5', 'anemail9@gail.com', 123456)
    assert user is not None
    # Second ensure that the user property shipping address is empty
    assert user.ship_addr == ''


def test_r1_9_user_register():
    '''
    Testing R1-9: Postal Code is empty at the time of registration
    '''
    # First assess that a newly registered user is valid
    user = register('user6', 'anemail10@gail.com', 123456)
    assert user is not None
    # Second ensure that the user property postal_code is empty
    assert user.postal_code == ''


def test_r1_10_user_register():
    '''
    Testing R1-10: Balance should be initialized as 100
    '''
    # First assess that a newly registered user is valid
    user = register('user7', 'anemail11@gail.com', 123456)
    assert user is not None
    # Second ensure that the user property balance is 100.0
    assert user.balance == 100.0


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have u0,
      u1 in database)
    '''
    # First assess that a newly made user is valid
    user = login('test0@test.com', 123456)
    assert user is not None
    # Second assess that the users username is the same as when registered
    assert user.username == 'us0'
    # Thirdly ensure that the user cannot log in with an incorrect password
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


def test_r3_2_update_user():
    '''
      Testing R3-2: Postal code should be non-empty, alphanumeric-only, and no special characters such as !.
    '''


def test_r3_3_update_user():
    '''
      Testing R3-3: Postal code has to be a valid Canadian postal code.
    '''


def test_r3_4_update_user():
    '''
      Testing R3-4: User name follows the requirements above.
    '''
