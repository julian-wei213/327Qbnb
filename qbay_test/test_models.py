from qbay.models import register, login

def test_r1_1_user_register():
    '''
    Testing R1-1: Email/Password cannot be empty
    '''
    assert register('user1', '0@email.com', 123456) is not None
    assert register('user2', '', 123456) is None

def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by their id
    '''

    user1 = register('user3' , '3@email.com',  123456)
    assert user1 is not None
    user2 = register('user4' , '4@email.com',  123456)
    assert user2 is not None
    assert user1.id != user2.id 


def test_r1_3_user_register():
    '''
    Testing R1-2: Email follows addr-spec defined by RFC 5322
    '''

    assert register('us2', 'an.eMa_il@gmail.uk.ca.com', 123456) is not None
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
    Testing R1-5: Username has to be non-empty, alpahnumerical, and space allowed only as prefix/suffix
    '''
    assert register('u U0', 'anemail1@gmail.com', 123456) is not None
    assert register(' uU0', 'anemail2@gmail.com', 123456) is None
    assert register('uU0 ', 'anemail3@gmail.com', 123456) is None
    assert register('', 'anemail4@gmail.com', 123456) is None

def test_r1_6_user_register():
    '''
    Testing R1-6: Username has to be more than 2 character and less than 20
    '''
    assert register('u', 'anemail5@gmail.com', 123456) is None
    assert register('us', 'anemail6@gmail.com', 123456) is None
    assert register('use', 'anemail6@gmail.com', 123456) is not None
    assert register('uabcdefghijklmnop123', 'anemail7@gmail.com', 123456) is None
    assert register('uabcdefghijklmnop12', 'anemail8@gmail.com', 123456) is not None


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''
    assert register('us0', 'test0@test.com', '123456') is not None
    assert register('us0', 'test1@test.com', '123456') is not None
    assert register('us1', 'test0@test.com', '123456') is None

def test_r1_8_user_register():
    '''
    Testing R1-8: Shipping Address is empty at the time of registration
    '''
    user = register('user5', 'anemail9@gail.com', 123456)
    assert user is not None
    assert user.ship_addr == ''

def test_r1_9_user_register():
    '''
    Testing R1-9: Postal Code is empty at the time of registration
    '''
    user = register('user6', 'anemail10@gail.com', 123456)
    assert user is not None
    assert user.postal_code == ''

def test_r1_10_user_register():
    '''
    Testing R1-10: Balance should be initialized as 100
    '''
    user = register('user7', 'anemail11@gail.com', 123456)
    assert user is not None
    assert user.balance == 100.0


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have u0,
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'us0'

    user = login('test0@test.com', 1234567)
    assert user is None
