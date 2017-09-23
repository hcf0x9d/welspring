#!/usr/bin/python3

# ==============================================================================
# Configuration

import googlemaps
import json
# import random
# import string
# import urllib

# import datetime
# import httplib2
# import requests

from functools import wraps
from config import Config

from flask import Flask, render_template, request  # , jsonify
from flask import redirect, url_for, flash  # , make_response
from flask import session as login_session
from flask_navigation import Navigation
from feeds import FeedReader, Twitter
from auth_controller import Authentication
from db_controller import DatabaseController

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
auth = Authentication()
twitter = Twitter()
db = DatabaseController()
nav = Navigation(app)
gmaps = googlemaps.Client(key=Config.API_KEYS['googleMaps'])

# Navigation
# TODO: Work on the navigation
nav.Bar('top', [

    nav.Item('Today\'s devotion', 'devotion_controller',
             html_attrs={'class': ['main-nav-target', 'mod-devotion'],
                         'role': 'menuitem'}),
    nav.Item('Find Schools', 'type_locator_controller',
             {'search_type': 'school'},
             html_attrs={'class': ['main-nav-target', 'mod-school'],
                         'role': 'menuitem'}),
    nav.Item('Find Churches', 'type_locator_controller',
             {'search_type': 'church'},
             html_attrs={'class': ['main-nav-target', 'mod-church'],
                         'role': 'menuitem'}),
    nav.Item('Goods & Services', 'connector_controller',
             html_attrs={'class': ['main-nav-target', 'mod-store'],
                         'role': 'menuitem'}),

])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session.get('user_id') is None:
            return redirect(url_for('login_controller', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# Routes

# TODO: [Views] Login/Authentication (AJAX)
@app.route('/login')
def login_controller():
    """Create an anti-forgery state token to assist security"""
    auth.create_session()
    print(login_session)
    return render_template('login.html', STATE=login_session['state'])


# TODO: [Views] Logout/Authentication (AJAX)
@app.route('/logout')
def logout_controller():
    return 'ajaxed'


# TODO: [Views] Home
@app.route('/')
def home_controller():
    returned_feed = FeedReader('verse').start()
    t = twitter.get_tweets('welstweets', 2)

    return render_template('index.html', verse_of_day=returned_feed,
                           tweets=t)


# TODO: [Views] Locator
@app.route('/locator')
def locator_controller():
    return render_template('locator.html')


# TODO: [Views] Locator
@app.route('/locator/<string:search_type>')
def type_locator_controller(search_type):
    print(search_type)
    return render_template('locator.html', term=search_type)


# TODO: [Views] Connector
@app.route('/connect')
def connector_controller():
    return render_template('connector.html')


# TODO: [Views] Devotion
@app.route('/grow/devotion')
def devotion_controller():
    returned_feed = FeedReader('devotion').start()
    t = twitter.get_tweets('welstweets', 2)
    return render_template('devotion.html', devotion=returned_feed, tweets=t)


# TODO: [Views] Connector
@app.route('/about')
def about_controller():
    return 'hello world'


# ==============================================================================
# Management routes


@app.route('/manage/venues')
@login_required
def venue_manager():
    venues = ''
    return render_template('admin/venues.html', venues=venues)


@app.route('/manage/venues/<string:venue_slug>')
@login_required
def venue_editor(venue_slug):
    venue = db.read_venue(venue_slug)
    return render_template('admin/venue.html', venue=venue)

# AJAX routes (CRUD)


@app.route('/create/venue', methods=['POST'])
@login_required
def venue_creator():
    # TODO: Create a venue script
    # Name and website are passed in
    db.create_venue(request.form)
    # db.add_item(request.form, login_session.get('user_id'))
    return json.dumps({'status': 'OK',
                       'post': request.form})


@app.route('/update/venue', methods=['POST'])
@login_required
def venue_updater():
    # TODO: Update a venue script
    return 'Update a venue'


@app.route('/delete/venue', methods=['POST'])
@login_required
def venue_deleter():
    # TODO: Delete a venue script
    return 'Delete a venue'


@app.route('/gconnect', methods=['POST'])
def gconnect():
    return auth.google_connection()


@app.route('/gdisconnect')
def gdisconnect(self):
    """Google Plus API disconnect/logout route"""
    return auth.logout()

# ==============================================================================
# API Endpoints


@app.route('/api/geocode', methods=['POST'])
def geocode_query():
    # Geocoding an address
    geocode_result = gmaps.geocode(request.form['search'])
    return json.dumps({'status': 'OK',
                      'response': geocode_result[0]['geometry']['location']})


@app.route('/api/place_details', methods=['POST'])
def place_detail():
    details = gmaps.place(request.form['id'])
    return json.dumps({'status': 'OK',
                       'response': details['result']})

# ==============================================================================


if __name__ == '__main__':
    # TODO: [DEPLOY TASKS] Make debug=False before deployment
    app.run(host='0.0.0.0', port=5000, debug=True)
