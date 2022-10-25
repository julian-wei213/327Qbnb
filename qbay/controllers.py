from flask import render_template, request, session, redirect
from qbay.models import login, User, Listing, register, create_listing
from qbay.models import update_listing
from datetime import date


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


@app.route('/update_listing', methods=['GET'])
def update_listing_get():
    """
    Function for Get commands
    """

    # Get all listings in database
    listings = Listing.query.order_by(Listing.id).all()

    # Render the template
    return render_template('update_listing.html', listings=listings,
                           message='')


@app.route('/update_listing', methods=['POST'])
def update_listing_post():
    """
    Function handling post commands for updating listing page
    """
    id = request.form.get('id')  # ID of the listing

    # Information to be passed for update
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price'))

    # Get the listing with the specific ID
    listing = Listing.query.filter_by(id=id).first()

    err_message = ''

    # Use backend update listing function
    success = update_listing(listing, title=title,
                             description=description, price=price)

    # If update failed update error message
    if not success:
        err_message = "List Update FAILED"

    if err_message:
        # If error message is not null render page with fail message
        listings = Listing.query.order_by(Listing.id).all()
        return render_template('update_listing.html',
                               listings=listings, message=err_message)
    else:
        # If update success update page with success message
        listings = Listing.query.order_by(Listing.id).all()
        return render_template('update_listing.html', listings=listings,
                               message="List Update PASSED")
