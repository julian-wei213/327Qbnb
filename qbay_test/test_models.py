from qbay.models import create_listing, register, login
from qbay.models import update_listing, User, Listing
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

    # 79 characters
    assert update_listing(listing, title='x' * 80) is not None

    # 80 characters
    assert update_listing(listing, title='x' * 81) is None

    # 1 character
    assert update_listing(listing, title='x' * 5) is not None

    # Description no less than 20 characters and no greater than 2000
    # characters

    # 20 characters
    assert update_listing(listing, description='x' * 20) is not None

    # 19 characters
    assert update_listing(listing, description='x' * 19) is None

    # 2000 characters
    assert update_listing(listing, description='x' * 2000) is not None

    # 2001 characters
    assert update_listing(listing, description='x' * 2001) is None

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
