#!/usr/bin/python3
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
    def create_venue(obj):
        new_venue = Venue(name=obj['name'], slug=obj['slug'],
                         website=obj['website'])
        session.add(new_venue)
        session.commit()
        return

    @staticmethod
    def read_venue(slug):
        venue = session.query(Venue) \
            .filter_by(slug=slug).one()
        return venue
