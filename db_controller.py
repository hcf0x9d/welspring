#!/usr/bin/python3
import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Base, Data, User, Venue, VenueSubType, VenueType

engine = create_engine('postgresql://welspring:password@localhost:5432'
                       '/welspring')
Base.metadata.bind = engine

database_session = sessionmaker(bind=engine)
session = database_session()


class DatabaseController:

    @staticmethod
    def create_user(auth_session):
        new_user = User(name=auth_session['name'], email=auth_session['email'],
                        picture=auth_session['picture'])
        session.add(new_user)
        session.commit()
        return

    def read_user(self, auth_session):
        try:
            user = session.query(User)\
                .filter_by(email=auth_session['email']).one()
            return user
        except:
            self.create_user(auth_session)
            return session.query(User)\
                .filter_by(email=auth_session['email']).one()

    @staticmethod
    def create_data_entry(entry_type, date, title, subtitle, body):
        entry = Data(type=entry_type, date=date, title=title,
                     subtitle=subtitle,
                     body=body)
        session.add(entry)
        session.commit()
        return

    @staticmethod
    def read_venue_list():
        venues = session.query(Venue).all()
        return venues

    @staticmethod
    def read_venue_list_by_search(state):
        venues = session.query(Venue).filter_by(state=state).all()
        return venues

    @staticmethod
    def create_venue(obj):
        new_venue = Venue(name=obj['name'],
                          slug=obj['slug'],
                          website=obj['website'],
                          address=obj['address'],
                          google_id=obj['google_id'],
                          location=obj['location'],
                          phone=obj['phone']
                          )

        session.add(new_venue)
        session.commit()
        return

    @staticmethod
    def read_venue(slug):
        venue = session.query(Venue) \
            .filter_by(slug=slug).one()
        return venue

    @staticmethod
    def read_venue_subtypes(venue_type):
        subtypes = session.query(VenueSubType)\
            .filter_by(venue_type_link=venue_type).all()
        return subtypes

    @staticmethod
    def update_venue(obj):
        venue = session.query(Venue) \
            .filter_by(slug=obj['v_edit_slug']).one()

        venue.name = obj['v_edit_name']
        venue.slug = re.sub('[^A-Za-z0-9]+', '-', obj['v_edit_name']).lower()
        venue.website = obj['v_edit_url']
        venue.admin_name = obj['v_edit_admin']
        venue.livestream = obj['v_edit_stream']
        venue.type_id = int(obj['v_edit_type'])
        if obj['v_edit_subtype'] != '':
            venue.sub_type_id = int(obj['v_edit_subtype'])
        # venue.service_time = obj['v_edit_service']
        venue.summary = obj['v_edit_summary'].strip()
        venue.picture = obj['v_edit_picture']
        venue.phone = obj['v_edit_phone']
        venue.address = obj['v_edit_address'].strip()

        session.commit()
        return
