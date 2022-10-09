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


def test_r3_1_update_user():
    '''
      Testing R3-1: A user is only able to update his/her user name, 
      user email, billing address, and postal code.
    '''
    # add user to database
    user = register('userr31', 'anemailr31@email.com', valid_password)
    new_name = "new " + user.username
    new_email = "new" + user.email
    new_address = "new" + user.ship_addr
    new_postal_code = "A1A 1A1"
    # update all posible fields
    user.update_name(new_name)
    user.update_email(new_email)
    user.update_address(new_address)
    user.update_postal_code(new_postal_code)
    # confirm they were changed
    assert user.username == new_name
    assert user.email == new_email
    assert user.ship_addr == new_address
    assert user.postal_code == new_postal_code


def test_r3_2_update_user():
    '''
      Testing R3-2: Postal code should be non-empty, alphanumeric-only, 
      and no special characters such as !.
    '''
    # confirm it works with valid postal code 
    user = register('userr32', 'anemailr32@email.com', valid_password)
    new_postal_code = "A1A 1A1"
    user.update_postal_code(new_postal_code)
    assert user.update_postal_code(new_postal_code) is True
    assert user.postal_code == new_postal_code
    # can't be empty
    new_postal_code = ""
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code
    # alphanumeric only
    new_postal_code = "A1A #A1"
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code


def test_r3_3_update_user():
    '''
      Testing R3-3: Postal code has to be a valid Canadian postal code.
      Follow style A1A 1A1
    '''
    # confirm works with valid canadian postal code
    user = register('userr33', 'anemailr33@email.com', valid_password)
    for i in range(100):
        new_postal_code = generate_canadian_postal_code()
        user.update_postal_code(new_postal_code)
        assert user.update_postal_code(new_postal_code) is True
        assert user.postal_code == new_postal_code
    # doesn't work with non-valid code
    new_postal_code = 'A1A A1A'
    user.update_postal_code(new_postal_code)
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code
    # example 2
    new_postal_code = 'A1A1A1'
    user.update_postal_code(new_postal_code)
    assert user.update_postal_code(new_postal_code) is False
    assert user.postal_code != new_postal_code


def generate_canadian_postal_code():
    code = ""
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += " "
    code += random.choice(string.digits)
    code += random.choice(string.ascii_uppercase)
    code += random.choice(string.digits)
    return code


def test_r3_4_update_user():
    '''
      Testing R3-4: User name follows the requirements above.
    '''
    user = register('userr34', 'emailr34@email.com', valid_password)
    # Confirm valid username is acceptable
    new_name = "test namer34"
    assert user.update_name(new_name) is True
    assert user.username == new_name
    # User name has to be non-empty
    new_name = ""
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # alphanumeric-only
    new_name = 'asd#f12!3'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # space allowed only if it is not as the prefix or suffix.

    # space in prefix should fail
    new_name = ' asdf123'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # space in suffix should fail
    new_name = 'asdf123 '
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # longer than 2 characters and less than 20 characters.

    # less than 3 should fail    
    new_name = '12'
    assert user.update_name(new_name) is False
    assert user.username != new_name
    # greater than 19 should fail
    new_name = ''.join(random.choice(string.ascii_letters) for i in range(20))
    print(new_name)
    assert user.update_name(new_name) is False
    assert user.username != new_name

