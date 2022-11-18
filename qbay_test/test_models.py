from qbay.models import register, login, check_str_contains_lower, \
    check_str_contains_upper, check_str_contains_special, update_listing, \
    User, Listing, create_listing
from datetime import date

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
    """
    Generates a random string of string_length
    """
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
    and space allowed only as non prefix/suffix
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


def test_user_register_fuzzy_test_param_1():
    '''
    Fuzzy testing for register() param 1

    Test fails if there exists a payload that causes an exception
    '''
    email = "fuzzyemail1@email.com"
    counter = 0

    with open('qbay_test/Generic_SQLI.txt') as f:
        for line in f.readlines():
            try:
                register(line, str(counter) + email, valid_password)
            except Exception:
                # Test has failed
                assert False
    assert True


def test_user_register_fuzzy_test_param_2():
    '''
    Fuzzy testing for register() param 2

    Test fails if there exists a payload that causes an exception
    (Note: this test takes a while)
    '''

    with open('qbay_test/Generic_SQLI.txt') as f:
        for line in f.readlines():
            print(line)
            try:
                register("username", line, valid_password)
            except Exception:
                # Test has failed
                assert False
    assert True


def test_user_register_fuzzy_test_param_3():
    '''
    Fuzzy testing for register() param 3

    Test fails if there exists a payload that causes an exception
    '''
    email = "fuzzyemail3@email.com"
    counter = 0

    with open('qbay_test/Generic_SQLI.txt') as f:
        for line in f.readlines():
            try:
                register("username", str(counter) + email, line)
            except Exception:
                # Test has failed
                assert False
    assert True


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
            assert login('r22%i@test.com' % (i), test_string) is not None
        else:
            register('ur22%i' % (i), 'r22%i@test.com'
                     % (i), test_string)
            assert login('r14%i@test.com' % (i), test_string) is None


def test_r3_1_update_user():
    '''
      Testing R3-1: A user is only able to update his/her user name,
      user email, billing address, and postal code.
    '''
    # add user to database
    user = register('userr31', 'anemailr31@email.com', valid_password)
    assert user is not None
    new_name = "new " + user.username
    new_email = "new" + user.email
    new_address = "new" + user.ship_addr
    new_postal_code = "A1A 1A1"
    # update all posible fields
    user.update_user(new_name, new_email, new_address, new_postal_code)

    # confirm they were changed
    user2 = login(new_email, valid_password)
    assert user2.username == new_name
    assert user2.email == new_email
    assert user2.ship_addr == new_address
    assert user2.postal_code == new_postal_code


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
    """
    Generates a random Canadian postal code
    """
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


def test_r4_1_create_listing():
    '''
    Testing R4-1: The title of the product has to be alphanumeric-only, and
      space allowed only if it is not as prefix and suffix.
    '''
    user = User.query.filter_by().first()

    # Case 1: Empty Title
    listing = create_listing('', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 2: Regular Title
    listing = create_listing('The Title', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 3: Regular Title with Numbers
    listing = create_listing('The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 4: Title with Space as Prefix
    listing = create_listing(' The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 5: Title with Space as Suffix
    listing = create_listing('The Title62 ', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 6: Title with Underscore
    listing = create_listing('The Tit_le', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_2_create_listing():
    '''
    Testing R4-2: The title of the product is no longer than 80 characters.
    '''
    user = User.query.filter_by().first()

    # Case 1: Title of 1 character
    listing = create_listing('A', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 2: Title of 80 characters
    listing = create_listing('x' * 80, 'description of listing' + 'x' * 80,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 3: Title of 81 characters
    listing = create_listing('x' * 81, 'description of listing' + 'x' * 81,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_3_create_listing():
    '''
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    user = User.query.filter_by().first()

    # Case 1: Description of 20 characters
    listing = create_listing('Title1', 'x' * 20,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 2: Description of 2000 characters
    listing = create_listing('Title2', 'x' * 2000,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 3: Description of 19 characters
    listing = create_listing('Title3', 'x' * 19,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 4: Description of 2001 characters
    listing = create_listing('Title4', 'x' * 2001,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 5: Description of arbitrary characters
    listing = create_listing('Title5', '  abc ABC 123 !@#  _~["',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None


def test_r4_4_create_listing():
    '''
    Testing R4-4: Description has to be longer than the product's title.
    '''
    user = User.query.filter_by().first()

    # Case 1: Description longer than title
    listing = create_listing('x' * 23, 'x' * 25,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 2: Description length equal to title length
    listing = create_listing('y' * 23, 'x' * 23,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 3: Description shorter than title
    listing = create_listing('z' * 23, 'x' * 21,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_5_create_listing():
    '''
    Testing R4-5: Price has to be of range [10, 10000].
    '''
    user = User.query.filter_by().first()

    # Case 1: Price = 10
    listing = create_listing('Title11', 'description of listing',
                             10, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 2: Price = 10000
    listing = create_listing('Title12', 'description of listing',
                             10000, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 3: Price = 50
    listing = create_listing('Title13', 'description of listing',
                             50, date(2022, 10, 6), user.id)
    assert listing is not None

    # Case 4: Price = 9.99
    listing = create_listing('Title14', 'description of listing',
                             9.99, date(2022, 10, 6), user.id)
    assert listing is None

    # Case 5: Price = 10000.01
    listing = create_listing('Title15', 'description of listing',
                             10000.01, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_6_create_listing():
    '''
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    '''
    user = User.query.filter_by().first()

    # Case 1: last_modified_date = 2021-01-03
    listing = create_listing('Title21', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None

    # Case 2: last_modified_date = 2025-01-01
    listing = create_listing('Title22', 'description of listing',
                             30.00, date(2025, 1, 1), user.id)
    assert listing is not None

    # Case 3: last_modified_date = 2023-01-01
    listing = create_listing('Title23', 'description of listing',
                             30.00, date(2023, 1, 1), user.id)
    assert listing is not None

    # Case 4: last_modified_date = 2021-01-02
    listing = create_listing('Title24', 'description of listing',
                             30.00, date(2021, 1, 2), user.id)
    assert listing is None

    # Case 5: last_modified_date = 2025-01-02
    listing = create_listing('Title25', 'description of listing',
                             30.00, date(2025, 1, 2), user.id)
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
    while not found_flag:
        for user in users:
            if user.id != testid:
                found_flag = True
                break
        if found_flag:
            break
        testid += 1

    listing = create_listing('Title31', 'description of listing',
                             30.00, date(2021, 1, 3), testid)
    assert listing is None

    # Case 2: owner_email is not empty
    register('tu0', 'testtu0@test.com', 'Abc#123')
    user = User.query.filter_by(username='tu0').first()

    listing = create_listing('Title32', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None

    # Case 3: owner_email is empty
    user.email = ''  # Potential Bug? Need to use update_user_profile

    listing = create_listing('Title33', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is None


def test_r4_8_create_listing():
    '''
    Testing R4-8: A user cannot create products that have the same title.
    '''
    user = User.query.filter_by().first()

    # Case 1: Same Title
    listing = create_listing('Title41', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    listing = create_listing('Title41', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)

    assert listing is None

    # Case 2: Different Title
    listing = create_listing('Title42', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None


def test_r5_1_update_listing():
    '''
    Testing R5-1: One can update all attributes of the listing,
    except owner_id and last_modified_date.
    '''
    listing = Listing.query.filter_by().first()

    # Test update title
    ntitle = "new title"
    assert (ntitle == listing.title) is False

    # Test whether listing.title got updated
    update_listing(listing, title=str(ntitle))
    assert (ntitle == listing.title) is True

    # Test update description
    long_description = "This is a detailed description with no grammar"
    assert (long_description == listing.description) is False

    # Test whether listing.description got updated
    update_listing(listing, description=str(long_description))
    assert (long_description == listing.description) is True

    # Test update price

    # Test price > 10000 constraint
    f = float(21000)
    assert update_listing(listing, price=f) is None

    # Test price < 10 constraint
    f = float(2)
    assert update_listing(listing, price=f) is None

    # Test whether listing.price got updated
    f = float(5000)
    assert update_listing(listing, price=f) is not None
    assert (float(5000) == listing.price) is True

    # Test multiple

    # Test update all three
    assert update_listing(listing, title="Three together",
                          description="There will be a total of three changes",
                          price=float(6000)) is not None

    # Check if update was implemented
    assert (listing.title == "Three together") is True
    assert (listing.description == "There will be a total of three changes")\
        is True
    assert (listing.price == 6000) is True

    # Test update all three, price fail
    assert update_listing(listing, title="Three together",
                          description="There will be a total of three changes",
                          price=float(500)) is None


def test_r5_2_update_listing():
    '''
    Testing R5-2: Price can be only increased but cannot be decreased :)
    '''
    listing = Listing.query.filter_by().first()

    # Check price decrease
    assert update_listing(listing, price=float(20)) is None
    assert (listing.price == 20) is False

    # Check price decrease
    assert update_listing(listing, price=float(6200)) is not None
    assert (listing.price == 6200) is True


def test_r5_3_update_listing():
    '''
    Testing R5-3: last_modified_date should be updated when
    the update operation is successful.
    '''
    listing = Listing.query.filter_by().first()

    # Check modified date
    update_listing(listing, title=str("title2"))
    assert (listing.last_modified_date == date.today()) is True


def test_r5_4_update_listing():
    '''
    Testing R5-4: When updating an attribute,
    one has to make sure that it follows the same requirements as above.
    '''
    listing = Listing.query.filter_by().first()

    # Title not alphanumeric
    assert update_listing(listing, title="%",
                          description="new stuff was written in here") is None

    # Space as prefix in title
    assert update_listing(listing, title=" title2",
                          description="new stuff was written in here") is None

    # Space as suffix in title
    assert update_listing(listing, title="title2 ",
                          description="new stuff was written in here") is None

    # Space as prefix and suffix in title
    assert update_listing(listing, title=" title2 ",
                          description="new stuff was written in here") is None

    # Space in middle of title
    assert update_listing(listing, title="ti tle2",
                          description="new stuff was written in") is not None

    # No Spaces
    assert update_listing(listing, title="title3",
                          description="new stuff was written in") is not None

    # Title less than 80 characters

    # 80 characters
    assert update_listing(listing, title='y' * 80) is not None

    # 81 characters
    assert update_listing(listing, title='y' * 81) is None

    # 5 characters
    assert update_listing(listing, title='y' * 5) is not None

    # Description no less than 20 characters and no greater than 2000
    # characters

    # 20 characters
    assert update_listing(listing, description='y' * 20) is not None

    # 19 characters
    assert update_listing(listing, description='y' * 19) is None

    # 2000 characters
    assert update_listing(listing, description='y' * 2000) is not None

    # 2001 characters
    assert update_listing(listing, description='y' * 2001) is None

    # Arbitrary numbers
    assert update_listing(listing, description='@*!&@ !@!+"{> :>>~ |":>DA>D')\
        is not None

    # Description must not be smaller than title

    # Smaller description than title
    short_description = "smo"
    assert update_listing(listing, description=short_description) is None

    # Larger description than title
    short_description = "This is a longer description then the other one"
    assert update_listing(listing, description=short_description) is not None

    # Price needs to in range [10, 10000], already did in r5-1

    # There can't be two listings with same title

    update_listing(listing, title="SAMETITLE")

    listing2 = Listing.query.filter_by(title="The Title62").first()

    # Same title case
    assert update_listing(listing2, title="SAMETITLE") is None

    # Different title case
    assert update_listing(listing2, title="Thishere") is not None
