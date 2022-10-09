from qbay.models import register, login, check_str_contains_lower, \
    check_str_contains_upper, check_str_contains_special
import string
import random

valid_password = 'Abc#123'


def test_r1_1_user_register():
    '''
    Testing R1-1: Email/Password cannot be empty
    '''
    # First assess that normal case works
    assert register('user1', '0@email.com', valid_password) is not None
    # Second ensure an empty email would fail
    assert register('user2', '', valid_password) is None
    # Third ensure an empty password would fail
    assert register('user3', '1@email.com', '') is None


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by their id
    '''
    # First assess that two new users are valid
    user1 = register('user3', '3@email.com', valid_password)
    assert user1 is not None
    user2 = register('user4', '4@email.com', valid_password)
    assert user2 is not None
    # Second make sure their id's are unique
    assert user1.id != user2.id


def test_r1_3_user_register():
    '''
    Testing R1-2: Email follows addr-spec defined by RFC 5322
    '''
    # First assess that the an email is valid given the constraints
    assert register('us2', 'an.eMa_il@gmail.uk.ca.com',
                    valid_password) is not None
    # Second test cases that must fail
    assert register('us2', 'im proper@gmail.com', valid_password) is None
    assert register('us2', 'improper@gmail..com', valid_password) is None
    assert register('us2', '.improper@gmail.com', valid_password) is None
    assert register('us2', 'improper@@gmail.com', valid_password) is None
    assert register('us2', 'improper@gmail.', valid_password) is None
    assert register('us2', 'improper@.com', valid_password) is None
    assert register('us2', '_improper@.com', valid_password) is None
    assert register('us2', 'i@mproper@.com', valid_password) is None


def test_r1_4_user_register():
    '''
    Testing R1-4: Password has to meet the required complexity:
    minimum length 6, at least one upper case, at least one lower case,
    and at least one special character.
    '''
    for i in range(100):
        string_length = random.randint(4, 10)
        test_string = generate_string(string_length)

        if (len(test_string) >= 6 and check_str_contains_lower(test_string)
            and check_str_contains_upper(test_string)
                and check_str_contains_special(test_string)):
            assert register('ur14%i' % (i), 'r14%i@test.com' %
                            (i), test_string) is not None
        else:
            assert register('ur14%i' % (i), 'r14%i@test.com' %
                            (i), test_string) is None


def generate_string(string_length):
    generated = ""
    for i in range(string_length):
        # pick an upper or lower case character
        letters = string.ascii_letters
        rng = random.randint(0, 10)
        # 10% of the time, pick a special character instead
        if rng >= 9:
            letters = string.punctuation
        generated += (random.choice(letters))
    return generated


def test_r1_5_user_register():
    '''
    Testing R1-5: Username has to be non-empty, alpahnumerical,
    and space allowed only as prefix/suffix
    '''
    # First assess that a username is valid based on the constraints
    assert register('u U0', 'anemail1@gmail.com', valid_password) is not None
    # Second test cases that need to fail
    assert register(' uU0', 'anemail2@gmail.com', valid_password) is None
    assert register('uU0 ', 'anemail3@gmail.com', valid_password) is None
    assert register('', 'anemail4@gmail.com', valid_password) is None


def test_r1_6_user_register():
    '''
    Testing R1-6: Username has to be more than 2 character and less than 20
    '''
    # First assess that the username is valid if within the constraint
    assert register('use', 'anemail6@gmail.com', valid_password) is not None
    assert register(
        'uabcdefghijklmnop12', 'email8@gmail.com', valid_password) is not None
    # Second assess that username is not valid if outside of constraint
    assert register('u', 'anemail5@gmail.com', valid_password) is None
    assert register('us', 'anemail6@gmail.com', valid_password) is None
    assert register(
        'uabcdefghijklmnop123', 'anemail7@gmail.com', valid_password) is None


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''
    # First create two usernames with two
    # different emails and that the operation is valid
    assert register('us0', 'test0@test.com', valid_password) is not None
    assert register('us0', 'test1@test.com', valid_password) is not None
    # Second attempt to make a new user with an already
    # used email and ensure its not valid
    assert register('us1', 'test0@test.com', valid_password) is None


def test_r1_8_user_register():
    '''
    Testing R1-8: Shipping Address is empty at the time of registration
    '''
    # First assess that a newly registered user is valid
    user = register('user5', 'anemail9@gail.com', valid_password)
    assert user is not None
    # Second ensure that the user property shipping address is empty
    assert user.ship_addr == ''


def test_r1_9_user_register():
    '''
    Testing R1-9: Postal Code is empty at the time of registration
    '''
    # First assess that a newly registered user is valid
    user = register('user6', 'anemail10@gail.com', valid_password)
    assert user is not None
    # Second ensure that the user property postal_code is empty
    assert user.postal_code == ''


def test_r1_10_user_register():
    '''
    Testing R1-10: Balance should be initialized as 100
    '''
    # First assess that a newly registered user is valid
    user = register('user7', 'anemail11@gail.com', valid_password)
    assert user is not None
    # Second ensure that the user property balance is 100.0
    assert user.balance == 100.0


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    '''
    # show that login works
    user_registered = register('userr21', 'emailr21@email.com', valid_password)
    user_log = login('emailr21@email.com', valid_password)
    assert user_log is not None
    assert user_log == user_registered


def test_r2_2_login():
    '''
    The login function should check if the supplied inputs meet the same
    email/password requirements as above, before checking the database.
    '''
    # This is hard to test here, I recommend checking models.py to confirm
    # that it doesn't bother querrying if requirements aren't met, but
    # will still show that it at least doesn't succeed in logging in.

    # create user to test login on
    register('userr22', 'emailr22@email.com', valid_password)

    # Confirm R1-1
    # Confirm that normal case works
    assert login('emailr21@email.com', valid_password) is not None
    # Ensure an empty email would fail
    assert login('', valid_password) is None
    # Ensure an empty password would fail
    assert login('emailr22@email.com', '') is None

    # Confirm R1-3
    # Login can't work with invalid email
    assert login('im proper@gmail.com', valid_password) is None
    assert login('improper@gmail..com', valid_password) is None
    assert login('.improper@gmail.com', valid_password) is None
    assert login('improper@@gmail.com', valid_password) is None
    assert login('improper@gmail.', valid_password) is None
    assert login('improper@.com', valid_password) is None
    assert login('_improper@.com', valid_password) is None
    assert login('i@mproper@.com', valid_password) is None
    assert login('im proper@gmail.com', valid_password) is None

    # Confirm R1-4
    # Login can't work with invalid password
    for i in range(100):
        string_length = random.randint(4, 10)
        test_string = generate_string(string_length)

        if (len(test_string) >= 6 and check_str_contains_lower(test_string)
            and check_str_contains_upper(test_string)
                and check_str_contains_special(test_string)):
            register('ur22%i' % (i), 'r22%i@test.com'
                     % (i), test_string)
            assert login('r22%i@test.com', test_string) is not None
        else:
            register('ur22%i' % (i), 'r22%i@test.com'
                     % (i), test_string)
            assert login('r14%i@test.com', test_string) is None
