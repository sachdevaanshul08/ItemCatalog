# Import Flask from flask library to make the flask application
from flask import Flask, jsonify, render_template
from flask import request, redirect, url_for, flash
# Import to maintain the login session
from flask import session as login_session
# Import to add additional header to the returned objects from the views.
from flask import make_response
# To use json
import json
# handles all steps of the OAuth 2.0 protocol
# required for making API call in Python
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
# Imports to make http calls
import httplib2
import requests
# Import to create the engine and session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
# Database tables (Classes)
from models import Base, User, Category, Item
import requests
# Logging
import logging

import random
import string

# Create the Flask instance with name of the running application as an argument
app = Flask(__name__)

logging.basicConfig(filename='usage.log', level=logging.DEBUG)

# Client ID issued by google to use in Oauth protocal
# to access the google apis server
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """
        Redirect the user on
        login page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/oauth/<provider>', methods=['POST'])
def gconnect(provider):
    """
        Exchange the one time auth code with
        access_token
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # STEP 1 - Parse the auth code
    auth_code = request.data.decode('utf-8')
    logging.info('Step 1 - Complete, received auth code %s' % auth_code)
    if provider == 'google':
        # STEP 2 - Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(
                'client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps(
                'Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = (
            'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'

        # # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(json.dumps(
                "Token's user ID doesn't match given user ID."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response = make_response(json.dumps(
                "Token's client ID does not match app's."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check if the user is already connected
        stored_access_token = login_session.get('access_token')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_access_token is not None and gplus_id == stored_gplus_id:
            response = make_response(json.dumps(
                'Current user is already connected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        logging.info('Step 2 Complete! Access Token : %s '
                     % credentials.access_token)

        # Store the access token in the session for later use.
        login_session['access_token'] = access_token
        login_session['gplus_id'] = gplus_id

        # STEP 3 - Find User or make a new one
        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)
        # Read the response from server
        data = answer.json()

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']

        # see if user exists, if it doesn't make a new one

        user_id = getUserID(login_session['email'])
        if not user_id:
            user_id = createUser(login_session)
        login_session['user_id'] = user_id

        output = ''
        output += '<h1>Welcome, '
        output += login_session['username']
        output += '!</h1>'
        output += '<img src="'
        output += login_session['picture']
        output += ''' " style = "width: 300px;
                    height: 300px;border-radius:
                    150px;-webkit-border-radius:
                    150px;-moz-border-radius: 150px;"> '''
        flash("you are now logged in as %s" % login_session['username'])
        return output
    else:
        return 'Unrecoginized Provider'


def createUser(login_session):
    """
        Create User
    """
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
        Return the exising user (if any)
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
        Return the user_id on the basis of email
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except exc.SQLAlchemyError:
        return None


# DISCONNECT - Revoke a current user's token
# and reset their login_session by removing all the cached data
@app.route('/gdisconnect')
def gdisconnect():
    """
        Disconnect from 3 party authenticator i.e. google in this app
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # response = make_response
        # (json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('catalog'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# @app.route("/deletecred")
# def deleteCred():
#     del login_session['access_token']
#     del login_session['gplus_id']
#     del login_session['username']
#     del login_session['email']
#     del login_session['picture']
#     return "delete"


# Catalog json
@app.route('/catalog.json')
def category_json():
    """
        return all the categories
        along with its items
    """
    category = session.query(Category).all()
    if not category:
        return jsonify({'message': 'no data found'})
    return jsonify(Category=[cat.serialize for cat in category])


# Menu.json
@app.route('/<int:cat_id>/item/JSON')
def item_json(cat_id):
    """
        return item(s) specific category
    """
    item = session.query(Item).filter_by(category_id=cat_id).all()
    if not item:
        return jsonify({'message': 'no data found'})
    return jsonify(Item=[it.serialize for it in item])


# Arbitrary Menu.json
@app.route('/<int:cat_id>/item/<int:item_id>/JSON')
def arbitraryitem_json(cat_id, item_id):
    """
        return speicific item under specific category
    """
    category = session.query(Category).filter_by(id=cat_id).first()
    if not category:
        return jsonify({'message': 'no category found with id %d' % cat_id})
    item = session.query(Item).filter_by(category_id=cat_id)\
                              .filter_by(id=item_id).first()
    if not item:
        return jsonify({'message': 'no item found'})
    return jsonify(Item=item.serialize)


# home page
@app.route('/')
@app.route('/home')
@app.route('/catalog')
def catalog():
    """
        Home page of the application
    """
    category = session.query(Category).all()
    item = session.query(Item).order_by(-Item.id).limit(len(category)).all()
    itemDetailsList = []
    for it in item:
        for cat in category:
            if cat.id == it.category_id:
                # if cat.name not in it.title:
                # it.title = it.title + " (" + cat.name + ")"
                itemDetailsList.append(ItemDetails(it.title, cat.name))
                # itemName.insert(iLoop, it.title + " (" + cat.name + ")")
    logging.info("fghj")
    return render_template('main.html',
                           Category=category,
                           Item=itemDetailsList, type=None)


# Fetch the items on the basis of category
@app.route('/catalog/<string:category_name>/items')
def item(category_name):
    """
        This will display Items under specific category
        on screen
    """
    category = session.query(Category).filter_by(name=category_name).first()
    item = session.query(Item).filter_by(
        category_id=category.id).order_by(Item.title).all()

    return render_template('main.html',
                           Category=session.query(Category).all(),
                           SelectedCategory=category.name, Item=item,
                           type="item")


# Fetch the item desciption on the basis of selected category and item
@app.route('/catalog/<string:category_name>/<string:item_name>')
def item_description(category_name, item_name):
    """
        Display the item description
    """
    if "(" in item_name:
        item_name = item_name.split(' (')[0]
    item = session.query(Item).filter_by(title=item_name).first()
    return render_template('item_description.html', Item=item)


# Edit Item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    """
        Edit Item
    """
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Item).filter_by(title=item_name).first()
    if not item.user_id or login_session['user_id'] != item.user_id:
        return "<script>function myFunction(){alert('You \
are not authorized to edit this item. Please create your own \
Item in order to edit items.');window.location='http://localhost:8000'}\
</script><body onload='myFunction()'>"

    if request.method == 'POST':
        # Check for title
        if request.form['title']:
            item.title = request.form['title']
        # Check for Description
        if request.form['description']:
            item.description = request.form['description']
        # Check for selected category
        if request.form['category']:
            category = session.query(Category).filter_by(
                name=request.form['category']).first()
            item.category_id = category.id
        session.add(item)
        session.commit()
        flash("Item Edited Successfully")
        return redirect(url_for('catalog'))
    else:
        category = session.query(Category).all()
        return render_template('edit_item.html', Category=category, Item=item)


@app.route('/catalog/add', methods=['GET', 'POST'])
def add_item():
    """
        Add Item
    """
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        # Check for title
        category = session.query(Category).filter_by(
            name=request.form['category']).first()
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=category.id,
                    user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        flash("Item Added Successfully")
        return redirect(url_for('catalog'))
    else:
        category = session.query(Category).all()
        return render_template('add_item.html', Category=category)


# Delete Item
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    """
        Delete Item
    """
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(Item).filter_by(title=item_name).first()
    if not item.user_id or login_session['user_id'] != item.user_id:
        return "<script>function myFunction(){alert('You \
are not authorized to delete this item. Please create your own \
Item in order to delete items.');window.location='http://localhost:8000'}\
</script><body onload='myFunction()'>"

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item deleted Successfully")
        return redirect(url_for('catalog'))
    else:
        category = session.query(Category).all()
        return render_template('delete_item.html', Item=item)


# To keep track itemname & category
class ItemDetails(object):
    def __init__(self, name=None, category=None):
        self.name = name
        self.category = category


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
