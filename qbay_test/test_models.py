from qbay.models import register, login, create_listing
from datetime import date


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


def test_r4_1_create_listing():
    '''
    Testing R4-1: The title of the product has to be alphanumeric-only, and
      space allowed only if it is not as prefix and suffix.
    '''
    # Case 1: Empty Title
    listing = create_listing('', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 2: Regular Title
    listing = create_listing('The Title', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Regular Title with Numbers
    listing = create_listing('The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 4: Title with Space as Prefix
    listing = create_listing(' The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 5: Title with Space as Suffix
    listing = create_listing('The Title62 ', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 6: Title with Underscore
    listing = create_listing('The Tit_le', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_2_create_listing():
    '''
    Testing R4-2: The title of the product is no longer than 80 characters.
    '''
    # Case 1: Title of 1 character
    listing = create_listing('A', 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 2: Title of 80 characters
    listing = create_listing('x' * 80, 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Title of 81 characters
    listing = create_listing('x' * 81, 'description of listing',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_3_create_listing():
    '''
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    # Case 1: Description of 20 characters
    listing = create_listing('Title', 'x' * 20,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 2: Description of 2000 characters
    listing = create_listing('Title', 'x' * 2000,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Description of 19 characters
    listing = create_listing('Title', 'x' * 19,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 4: Description of 2001 characters
    listing = create_listing('Title', 'x' * 2001,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 5: Description of arbitrary characters
    listing = create_listing('Title', '  abc ABC 123 !@#  _~["',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
