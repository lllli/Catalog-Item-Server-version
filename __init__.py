from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash
from flask import session as login_session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from setup_db import base, Platform, Game, User
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import httplib2
import json
import requests
from functools import wraps


#login_session.clear()
#login_session = {}
CLIENT_ID = json.loads(
    open(r'/var/www/catalog/catalog/client_server.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item App"
app = Flask(__name__)
engine = create_engine('postgresql://catalog:password@localhost/catalog')
base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')


def login_required(f):
    """ Checks if the user is logged in or not """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You need to be logged in to add a new item.")
            return redirect(url_for('get_index_page'))
    return decorated_function

@app.route('/gconnect', methods=['POST'])
def gconnect():
    print 'start of gconnect'
    if request.args.get('state') !=login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets(r'/var/www/catalog/catalog/client_server.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dump('Failed to upgrade the authorization code.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')),50)
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
    if result['user_id']!=gplus_id:
        response = make_response(json.dump("Token's user ID doesn't match given user ID."),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to']!=CLIENT_ID:
        response = make_response(json.dump("Token's client ID doesn't match given client ID."),401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('current user is already connected'),200)
        response.headers['Content-Type'] = 'application/json'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    print 'before userinfo_url'
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session['username'] = data['name']
    #login_session['picture'] = data['picture']
    #login_session['email'] = data['email']
    #user_id = getUserID(login_session['email'])
    #if not user_id:
        #user_id = createUser(login_session)
    #login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    #output += login_session['username']
    output += '!</h1>'
    #output += '<img src="'
    #output += login_session['picture']
    #output += '"style = "width:300px; height:300px; border-radius: 150px;-webkit-borer-radius: 150px;-moz-border-radius:150px;">'
    flash("you are now logged in as %s"%login_session['username'])
    return redirect(url_for(get_index_page))    #return output
'''
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(name=login_session['username']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
'''

def title_exist(title):
    """ Checks if an item exists with the same unique title in db """
    results = session.query(Game).filter_by(title=title).all()
    return len(results) > 0


@app.route('/')
def go_main():
    """ Main Page """
    return redirect(url_for('get_index_page'))


@app.route('/catalog/JSON')
def get_platform():
    """ Returns JSON version of the catalog """
    output = []
    platforms = session.query(Platform).all()
    for platform in platforms:
        games = session.query(Game).filter_by(platform_id=platform.id)
        category_output = {}
        category_output["id"] = platform.id
        category_output["name"] = platform.name
        category_output["games"] = [game.serialize for game in games]
        output.append(category_output)
    return jsonify(Platforms=output)


@app.route('/catalog', methods=['GET','POST'])
def get_index_page():
    """ Handler for main page, includes auth, session management """
    #login_session.clear()
    try:
        user = login_session['username']
        print user
    except KeyError:
        user = None
    if request.method == 'GET':
        STATE = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        login_session['state'] = STATE
        platforms = session.query(Platform).all()
        latest_games = session.query(Game).order_by(desc(Game.date)).all()
        platform_names = {}
        for platform in platforms:
            platform_names[platform.id] = platform.name
        if len(latest_games) == 0:
            flash("No items found")
        return render_template(
            'main.html', platforms=platforms, games=latest_games,
            platform_names=platform_names, user=user, STATE=STATE, login_session=login_session
        )
    else:
        print ("Starting authentication")
	if request.args.get('state') != login_session['state']:
            response = make_response(json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        # Obtain authorization code
        auth_code = request.data
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(r'/var/www/catalog/catalog/client_server.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
	print 'after get credentials'
        # Check that the access token is valid.
        #login_session['credentials']=credentials
	access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
	    return response
        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            response = make_response(json.dumps("Token's client ID does not match app's."), 401)
            print "Token's client ID does not match app's."
            response.headers['Content-Type'] = 'application/json'
            return response
	stored_access_token = login_session.get('access_token')
        #stored_credentials = login_session.get('credentials')
        stored_gplus_id = login_session.get('gplus_id')
        #if stored_credentials is not None and gplus_id == stored_gplus_id:
        if stored_access_token is not None and gplus_id == stored_gplus_id:
	    response = make_response(json.dumps('Current user is already connected.'),200)
            response.headers['Content-Type'] = 'application/json'
            return response
	print 'at line 231'
        # Store the access token in the session for later use.
        #login_session['credentials']=credentials
	if credentials is None:
            response = make_response(json.dumps('credential is none'),200)
            response.headers['Content-Type']='application/json'
	    return response
	login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id
	login_session['provider'] = 'google'
	#if login_session['access_token'] is None:    
        #    response = make_response(json.dumps('get before get user info,access token is none',200))
	#    return response
        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)
        data = json.loads(answer.text)
	print 'at line 248'
        login_session['username'] = data['name']
        flash("you are now logged in as %s" % login_session['username'])
        #gconnect()
	print 'before return'
        return redirect(url_for('get_index_page'))

@app.route('/catalog/categories/<platform_name>/')
def get_games(platform_name):
    """ Returns items for a given category name """
    platforms = session.query(Platform).all()
    selected_platform = session.query(Platform).filter_by(name=platform_name).one()
    games = session.query(Game).filter_by(platform_id=selected_platform.id).order_by(desc(Game.date)).all()
    platform_names = {}
    for platform in platforms:
        platform_names[platform.id] = platform.name
    if len(games) == 0:
        flash("No items found in this category")
    try:
        user = login_session['username']
    except KeyError:
        user = None
    return render_template('platform_detail.html', selected_platform=selected_platform,  user=user, games=games, platforms=platforms, platform_name=platform_names)


@app.route('/catalog/items/<game_title>/')
def getItemDetails(game_title):
    """ Returns a specific item object given its title """
    game = session.query(Game).filter_by(title=game_title).one()
    platform = session.query(Platform).filter_by(id=game.platform_id).one()
    return render_template('game_detail.html', game=game, platform=platform)


@app.route('/catalog/items/new', methods=['GET', 'POST'])
@login_required
def new_game():
    """ Handles the creation of a new item """
    platforms = session.query(Platform).all()
    try:
        user = login_session['username']
    except KeyError:
        user = None
    if request.method == 'POST':
        title = request.form['title']
        if title_exist(title):
            flash("Please enter a different title. Item " + title + " already exists.")
            return redirect(url_for('newItem'))
        newItem = Game(title,
            request.form['description'],
            request.form['cover'],
            request.form['release'],
            request.form['platform_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('get_index_page'))
    else:
        return render_template('create_game.html', platforms=platforms, user=user)


@app.route('/catalog/items/<game_title>/edit', methods=['GET', 'POST'])
@login_required
def edit_game(game_title):
    """ Handles updating an existing item """
    edited_game = session.query(Game).filter_by(title=game_title).one()
    platform = session.query(Platform).filter_by(id=edited_game.platform_id).one()
    platforms = session.query(Platform).all()
    if request.method == 'POST':
        if request.form['title']:
            title = request.form['title']
            if game_title != title and title_exist(title):
                flash("Please enter a different title. Item " + title + " already exists.")
                return redirect(url_for('editItem', game_title=game_title))
            edited_game.title = title
        if request.form['description']:
            edited_game.description = request.form['description']
        if request.form['cover']:
            edited_game.cover = request.form['cover']
        if request.form['release']:
            edited_game.release = request.form['release']
        if request.form['platform_id']:
            edited_game.platform_id = request.form['platform_id']
        session.add(edited_game)
        session.commit()
        return redirect(url_for('get_index_page'))
    else:
        user = login_session['username']
        return render_template('edit_game.html', game=edited_game, platform=platform, platforms=platforms, user=user)

@app.route('/catalog/items/<game_title>/delete', methods=['GET', 'POST'])
@login_required
def delete_game(game_title):
    """ Deletes an item given its unique title """
    if request.method == 'POST':
        del_item = session.query(Game).filter_by(title=game_title).one()
        session.delete(del_item)
        session.commit()
        return redirect(url_for('get_index_page'))
    else:
        user = login_session['username']
        #user = 'kimi'
        return render_template('delete_game.html', game_title = game_title, user=user)


@app.route('/gdisconnect')
def gdisconnect():
    '''
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current User Not connected.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    """ Helper for disconnecting from Google Auth """
    '''
    '''
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session['username']
    
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected. No access token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
   
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result
    #result['status'] = '200'
    if result['status'] == '200':
        #del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('get_index_page'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    '''
    access_token = login_session['access_token']
    if access_token is None:
        print 'Access token is None'
        response = make_response(json.dumps
                                 ('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token
    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[  # noqa
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # The given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        del login_session['gplus_id']
	del login_session['access_token']
	del login_session['username']
	del login_session['provider']
	return redirect(url_for('get_index_page'))
if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run()
