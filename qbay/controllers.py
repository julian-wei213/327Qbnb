from flask import render_template, request, session, redirect
from qbay.models import login, User, Listing, register
from qbay.models import update_listing, create_listing, create_booking
from datetime import date, datetime


from qbay import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    """
    Handles get command for login page
    """
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    """
    Handles post command for login page
    """
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # some fake product data
    products = [
        {'name': 'prodcut 1', 'price': 10},
        {'name': 'prodcut 2', 'price': 20}
    ]
    return render_template('index.html', user=user, products=products)


@app.route('/register', methods=['GET'])
def register_get():
    """
    Handles get command for register page
    """
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    """
    Handles post command for register page
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/profile_update', methods=['GET'])
def profile_update_get():
    """
    Handles get command for profile update page
    """
    # access user by quering for the email in the current session
    user = User.query.filter_by(email=session['logged_in']).first()
    # render the profile_update html page when linked to /profile_update
    username = user.username
    email = user.email
    bill = user.ship_addr
    postal = user.postal_code

    if bill == '':
        bill = "You have yet to set a billing address"
    if postal == '':
        postal = "You have yet to set a postal code"

    # use user data to display current placeholders
    return render_template('profile_update.html',
                           message='',
                           user_name_placeholder=username,
                           user_email_placeholder=email,
                           user_bill_placeholder=bill,
                           user_postal_placeholder=postal)


@app.route('/profile_update', methods=['POST'])
def profile_update_post():
    """
    Handles post command for profile update page
    """
    username = request.form.get('name')
    email = request.form.get('email')
    bill = request.form.get('bill_addr')
    postal = request.form.get('postal_code')

    # Custom messages
    err_msg = 'Invalid Input, Please Try Again!'
    success_msg = 'Profile Updated!'

    # access user by quering for the email in the current session
    user = User.query.filter_by(email=session['logged_in']).first()

    # Update only the text boxes that were filled
    if username == '':
        username = user.username
    if email == '':
        email = user.email
    if bill == '':
        bill = user.ship_addr
    if postal == '':
        postal = user.postal_code

    # Check for success after updated database
    success = user.update_user(username=username, email=email,
                               ship_addr=bill, postal_code=postal)

    # If success render html
    if success:
        session['logged_in'] = user.email
        return render_template('profile_update.html',
                               message=success_msg,
                               user_name_placeholder=user.username,
                               user_email_placeholder=user.email,
                               user_bill_placeholder=user.ship_addr,
                               user_postal_placeholder=user.postal_code)
    else:
        # If fail, add error message to indicate failure
        return render_template('profile_update.html',
                               message=err_msg,
                               user_name_placeholder=user.username,
                               user_email_placeholder=user.email,
                               user_bill_placeholder=user.ship_addr,
                               user_postal_placeholder=user.postal_code)


@app.route('/booking', methods=['GET'])
def booking_get():
    """
    Handles get command for booking page
    """
    listings = Listing.query.order_by(Listing.id).all()
    return render_template('booking.html',
                           listings=listings,
                           message='')


@app.route('/booking', methods=['POST'])
def booking_post():
    """
    Handles post command for booking page
    """

    l_id = int(request.form.get('l_id'))
    start_date = datetime.strptime(request.form.get('start_date'),
                                   '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form.get('end_date'),
                                 '%Y-%m-%d').date()

    # Custom messages
    err_msg = 'Invalid Input, Please Try Again!'
    success_msg = 'Listing Booked!'

    # access user by quering for the email in the current session
    user = User.query.filter_by(email=session['logged_in']).first()
    # access list of listings
    listings = Listing.query.order_by(Listing.id).all()

    # Check for success after booking
    success = create_booking(user_id=user.id, listing_id=l_id,
                             start_date=start_date, end_date=end_date)

    # If success render html
    if success:
        return render_template('booking.html',
                               listings=listings,
                               message=success_msg)
    else:
        return render_template('booking.html',
                               listings=listings,
                               message=err_msg)


@app.route('/create_listing', methods=['GET'])
def create_listing_get():
    """
    Handles get command for create listing page
    """
    # templates are stored in the templates folder
    listings = Listing.query.order_by(Listing.id).all()
    return render_template('create_listing.html',
                           listings=listings, message='')


@app.route('/create_listing', methods=['POST'])
def create_listing_post():
    """
    Handles post command for create listing page
    """
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price'))

    error_message = None

    user_id = User.query.filter_by(email=session['logged_in']).first().id
    # use backend api to create listing
    success = create_listing(title, description, price, date.today(), user_id)
    if not success:
        error_message = "Listing Creation failed."

    # Display error message if listing creation failed.
    # Otherwise, display confirmation message.
    listings = Listing.query.order_by(Listing.id).all()
    if error_message:
        return render_template('create_listing.html', listings=listings,
                               message=error_message)
    else:
        return render_template('create_listing.html', listings=listings,
                               message='Listing Creation succeeded!')


@app.route('/logout')
def logout():
    """
    Logout page
    """
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/listing', methods=['GET'])
def listing():
    """
    function handling the GET method for /listing
    """
    # Get the id of the logged on user
    user_id = User.query.filter_by(email=session['logged_in']).first().id

    # Get all listings in database
    listings = Listing.query.filter_by(owner_id=user_id).all()

    # load the template
    return render_template('listing.html', listings=listings,
                           message='Here are all your listings')


@app.route('/listing/update/<int:id>', methods=['GET'])
def update_listing_get(id):
    """
    Function for Get commands
    """
    # Get all listings in database
    listing = Listing.query.filter_by(id=id).all()

    # Render the template
    return render_template('update_listing.html', listing=listing,
                           message='')


@app.route('/listing/update/<int:id>', methods=['POST'])
def update_listing_post(id):
    """
    Function handling post commands for updating listing page
    """
    # Information to be passed for update
    title = request.form.get('title')
    description = request.form.get('description')

    # Check if any of the inputs are empty
    if (request.form.get('price') == ""):
        price = None
    else:
        price = float(request.form.get('price'))

    if (title == ""):
        title = None
    if (description == ""):
        description = None

    # Get the listing with the specific ID
    listing = Listing.query.filter_by(id=id).first()

    err_message = ''

    # Use backend update listing function
    success = update_listing(listing, title=title,
                             description=description, price=price)

    # If update failed update error message
    if not success:
        err_message = "List Update FAILED"

    # Change the listing to reflect changes
    listing = Listing.query.filter_by(id=id).all()

    if err_message:
        # If error message is not null render page with fail message
        return render_template('update_listing.html',
                               listing=listing, message=err_message)
    else:
        # If update success update page with success message
        return render_template('update_listing.html', listing=listing,
                               message="List Update PASSED")
