#!/usr/bin/python3

# ==============================================================================
# Configuration

import googlemaps
import random
import string
import urllib

import datetime
# import httplib2
import json
# import requests

from config import Config
from flask import Flask, render_template, request, jsonify
# from flask import redirect, url_for, flash, make_response
# from flask import session as login_session
from flask_navigation import Navigation
from feeds import FeedReader

app = Flask(__name__)
# TODO: [Before Release] Change the password in production
# app.config['DATABASE'] = 'postgresql://welspring:password@localhost/welspring'

# TODO: [Before Release] Update the app secret key to a static guid
app.config['SECRET_KEY'] = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for x in range(32))

# db = DatabaseController()
nav = Navigation(app)
gmaps = googlemaps.Client(key=Config.API_KEYS['googleMaps'])

# Navigation
# TODO: Work on the navigation
nav.Bar('top', [
    nav.Item('Home', 'home_controller', items=[
        nav.Item('Daily Devotion', 'devotion_controller'),
        nav.Item('Connector', 'connector_controller'),
    ]),
    nav.Item('Locator', 'locator_controller', items=[
        nav.Item('Schools', 'type_locator_controller',
                 {'search_type': 'school'}),
        nav.Item('Churches', 'type_locator_controller',
                 {'search_type': 'church'}),
    ]),
])


# ==============================================================================
# Routes

# TODO: [Views] Login/Authentication (AJAX)
@app.route('/login')
def login_controller():
    return 'ajaxed'


# TODO: [Views] Logout/Authentication (AJAX)
@app.route('/logout')
def logout_controller():
    return 'ajaxed'


# TODO: [Views] Home
@app.route('/')
def home_controller():
    returned_feed = FeedReader('verse').start()
    return render_template('index.html', verse_of_day=returned_feed)


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
    return render_template('devotion.html', devotion=returned_feed)


# TODO: [Views] Connector
@app.route('/about')
def about_controller():
    return 'hello world'

# ==============================================================================
# AJAX Endpoints / API Endpoints


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
