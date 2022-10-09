from qbay.models import register
import string
import random

valid_password = 'Abc#123'


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

