from qbay.models import register, login, create_listing
from datetime import date
from qbay.models import User


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
    listing = create_listing('x' * 80, 'description of listing' + 'x' * 80,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Title of 81 characters
    listing = create_listing('x' * 81, 'description of listing' + 'x' * 81,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_3_create_listing():
    '''
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    # Case 1: Description of 20 characters
    listing = create_listing('Title1', 'x' * 20,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 2: Description of 2000 characters
    listing = create_listing('Title2', 'x' * 2000,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Description of 19 characters
    listing = create_listing('Title3', 'x' * 19,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 4: Description of 2001 characters
    listing = create_listing('Title4', 'x' * 2001,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 5: Description of arbitrary characters
    listing = create_listing('Title5', '  abc ABC 123 !@#  _~["',
                             30.00, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_4_create_listing():
    '''
    Testing R4-4: Description has to be longer than the product's title.
    '''
    # Case 1: Description longer than title
    listing = create_listing('x' * 23, 'x' * 25,
                             30.00, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 2: Description length equal to title length
    listing = create_listing('y' * 23, 'x' * 23,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 3: Description shorter than title
    listing = create_listing('z' * 23, 'x' * 21,
                             30.00, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_5_create_listing():
    '''
    Testing R4-5: Price has to be of range [10, 10000].
    '''
    # Case 1: Price = 10
    listing = create_listing('Title1', 'description of listing',
                             10, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 2: Price = 10000
    listing = create_listing('Title2', 'description of listing',
                             10000, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 3: Price = 50
    listing = create_listing('Title3', 'description of listing',
                             50, date(2022, 10, 6), 0)
    assert listing is not None
    
    # Case 4: Price = 9.99
    listing = create_listing('Title4', 'description of listing',
                             9.99, date(2022, 10, 6), 0)
    assert listing is None
    
    # Case 5: Price = 10000.01
    listing = create_listing('Title5', 'description of listing',
                             10000.01, date(2022, 10, 6), 0)
    assert listing is None


def test_r4_6_create_listing():
    '''
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    '''
    # Case 1: last_modified_date = 2021-01-03
    listing = create_listing('Title1', 'description of listing',
                             30.00, date(2021, 1, 3), 0)
    assert listing is not None
    
    # Case 2: last_modified_date = 2025-01-01
    listing = create_listing('Title2', 'description of listing',
                             30.00, date(2025, 1, 1), 0)
    assert listing is not None
    
    # Case 2: last_modified_date = 2023-01-01
    listing = create_listing('Title3', 'description of listing',
                             30.00, date(2023, 1, 1), 0)
    assert listing is not None
    
    # Case 2: last_modified_date = 2021-01-02
    listing = create_listing('Title4', 'description of listing',
                             30.00, date(2021, 1, 2), 0)
    assert listing is None
    
    # Case 2: last_modified_date = 2025-01-02
    listing = create_listing('Title5', 'description of listing',
                             30.00, date(2025, 1, 2), 0)
    assert listing is None


def test_r4_7_create_listing():
    '''
    Testing R4-7: owner_email cannot be empty. The owner of the
      corresponding product must exist in the database.
    '''    
    # Case 1: owner is not in database
    users = User.query.all()
    testid = 0
    found_flag = False
    while found_flag:
        for user in users:
            if user.id != testid:
                found_flag = True
                break
        if found_flag: 
            break
        testid += 1
    
    listing = create_listing('Title1', 'description of listing',
                             30.00, date(2021, 1, 3), testid)
    assert listing is None
    
    # Case 2: owner_email is not empty
    register('tu0', 'testtu0@test.com', '123456')
    user = User.query.filter_by(username='tu0').first()
    
    listing = create_listing('Title2', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None
    
    # Case 3: owner_email is empty
    user.email = ''  # Potential Bug? Need to use update_user_profile
    
    listing = create_listing('Title3', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is None


def test_r4_8_create_listing():
    '''
    Testing R4-8: A user cannot create products that have the same title.
    '''    
    # Case 1: Same Title
    listing = create_listing('Title1', 'description of listing',
                             30.00, date(2021, 1, 3), 0)
    listing = create_listing('Title1', 'description of listing',
                             30.00, date(2021, 1, 3), 0)
    assert listing is None
    
    # Case 2: Different Title
    listing = create_listing('Title2', 'description of listing',
                             30.00, date(2021, 1, 3), 0)
    assert listing is not None
