from qbay import app
from qbay.models import *
from qbay.controllers import *

"""
This file runs the server at a given port
"""

FLASK_PORT = 8081

if __name__ == "__main__":
    # Create some test people
    user1 = {'email': 'user1@gmail.com', 'password': 'user1Pass!'}
    user2 = {'email': 'user2@gmail.com', 'password': 'user2Pass!'}
    user3 = {'email': 'user3@gmail.com', 'password': 'user3Pass!'}
    user4 = {'email': 'user4@gmail.com', 'password': 'user4Pass!'}

    register('user1', user1['email'], user1['password'])
    register('user2', user2['email'], user2['password'])
    register('user3', user3['email'], user3['password'])
    register('user4', user4['email'], user4['password'])

    # login(user1['email'], user1['password'])

    app.run(debug=True, port=FLASK_PORT)
