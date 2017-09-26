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

# SET KEYS
app.config['SECRET_KEY'] = Config.SECRET_KEY
gmaps = googlemaps.Client(key=Config.API_KEYS['googleMaps'])

# INITIALIZE CLASSES
auth = Authentication()
twitter = Twitter()
db = DatabaseController()
nav = Navigation(app)


# Navigation
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

nav.Bar('admin', [
    nav.Item('Venues', 'venue_manager')
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


@app.route('/')
def home_controller():
    """Build and render the home page

    :return: Template engine with verse of the day and tweets as vars
    """
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


@app.route('/grow/devotion')
def devotion_controller():
    """Build and render the devotion view

    Need to grab the devotion from WELS.net as well as the latest tweets from
    the welstweets account

    :return: Render template with devotion object and tweets
    """
    returned_feed = FeedReader('devotion').start()
    t = twitter.get_tweets('welstweets', 2)
    return render_template('devotion.html', devotion=returned_feed, tweets=t)


# TODO: [Views] About the welspring
@app.route('/about')
def about_controller():
    return 'hello world'


# ==============================================================================
# Management routes

# MANAGE CONNECTOR ITEMS


@app.route('/manage/connector')
@login_required
def connector_manager():
    # TODO: Connector Management
    return render_template('admin/venues.html')


@app.route('/manage/connector/<string:connector_slug>')
@login_required
def connector_editor(connector_slug):
    # TODO: Connector Management
    print(connector_slug)
    return render_template('admin/venues.html')


# MANAGE VENUES


@app.route('/manage/venues')
@login_required
def venue_manager():
    venues = db.read_venue_list()

    school_checked = ''
    church_checked = ''

    return render_template('admin/venues.html', venues=venues,
                           school_checked=school_checked,
                           church_cheched=church_checked)


@app.route('/manage/venues/<string:venue_slug>')
@login_required
def venue_editor(venue_slug):
    venue = db.read_venue(venue_slug)

    school_checked = ''
    church_checked = ''
    sub_dd = ''
    subtypes = ''
    picture = ''

    if venue.type_id == 2:
        church_checked = 'checked'
        subtypes = db.read_venue_subtypes(venue_type=2)
    elif venue.type_id == 1:
        school_checked = 'checked'
        subtypes = db.read_venue_subtypes(venue_type=1)

    if venue.picture is not None:
        picture = venue.picture
    else:
        picture = '#'

    for option in subtypes:
        checked = ''

        if venue.sub_type_id == option.id:
            checked = 'selected'

        sub_dd += '<option value="%s" %s>%s</option>' % (option.id,
                                                         checked, option.name)
    print(sub_dd)
    return render_template('admin/venue.html', venue=venue,
                           sch_chkd=school_checked,
                           cch_chkd=church_checked,
                           subtype_dd=sub_dd,
                           pic=picture)


# AJAX ROUTES (CRUD)


@app.route('/create/venue', methods=['POST'])
@login_required
def venue_creator():
    """AJAX Route for creating a venue

    Creation of the venue only requires two fields, a name and website. The AJAX
    form then builds a url slug and after a successful DB insert, the returned
    object sends the slug back and the user is redirected to edit the rest of
    the fields.

    :return: JSON Object
    """
    print(request.form)
    db.create_venue(request.form)
    return json.dumps({'status': 'OK',
                       'post': request.form})


@app.route('/update/venue', methods=['POST'])
@login_required
def venue_updater():
    update = db.update_venue(request.form)
    # TODO: Update a venue script
    return json.dumps({'status': 'OK',
                      'response': update})


@app.route('/delete/venue', methods=['POST'])
@login_required
def venue_deleter():
    # TODO: Delete a venue script
    return 'Delete a venue'


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Google Pllus API Connection route"""
    return auth.google_connection()


@app.route('/gdisconnect')
def gdisconnect():
    """Google Plus API disconnect/logout route"""
    return auth.logout()


# ==============================================================================
# API Endpoints


@app.route('/api/getVenueSubTypes', methods=['POST'])
def get_venue_subtypes():
    subtypes = db.read_venue_subtypes(request.form['id'])

    obj = {}

    for idx, row in enumerate(subtypes):
        obj[row.name] = row.id

    return json.dumps({'status': 'OK',
                       'response': obj})


@app.route('/api/geocode', methods=['POST'])
def geocode_query():
    # Geocoding an address
    geocode_result = gmaps.geocode(request.form['search'])
    return json.dumps({'status': 'OK',
                      'response': geocode_result[0]['geometry']['location']})


@app.route('/api/venues', methods=['POST'])
def api_venue_list():
    print('venue list')
    list = db.read_venue_list_by_search(request.form['state'])

    return json.dumps({'status': 'OK',
                       'response': [venue.serialize for venue in list]})


@app.route('/api/place_details', methods=['POST'])
def place_detail():
    details = gmaps.place(request.form['id'])
    venue = db.read_venue(request.form['slug'])

    return json.dumps({'status': 'OK',
                       'gmaps': details['result'],
                       'welspring': venue.serialize })


# ==============================================================================


if __name__ == '__main__':
    # TODO: [DEPLOY TASKS] Make debug=False before deployment
    app.run(host='0.0.0.0', port=5000, debug=True)
