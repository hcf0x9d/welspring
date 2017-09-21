#!/usr/bin/python3

# Configuration ============================================================== #
from config import Config
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Data(Base):

    __tablename__ = 'datastore'

    id = Column(Integer, primary_key=True)
    # e.g. devotion, votd, etc.
    type = Column(String(64), nullable=False, index=True)
    # Date provide programmatically, not by the DB
    date = Column(String(64), nullable=False)
    # String or stringified object
    title = Column(String(250))
    subtitle = Column(String(250))
    body = Column(Text)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'date': self.date,
            'title': self.title,
            'subtitle': self.subtitle,
            'body': self.body
        }


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(250))
    password_hash = Column(String(64))


# class Venue(Base):
#
#     __tablename__ = 'venue'
#
#     id = Column(Integer, primary_key=True)
#     google_id = Column(String(64), nullable=False, index=True)
#     # Church or school
#     name = Column(String(250), nullable=False)
#     # lat/lng string from google
#     location = Column(String(250), nullable=False)
#     # HTML entry with spans like Google's API
#     address = Column(String(250), nullable=False)
#     type_id = Column(Integer, ForeignKey('venue_type.id'))
#     venue_type = relationship(VenueType)
#     sub_type_id = Column(Integer, ForeignKey('venue_sub_type.id'))
#     venue_sub_type = relationship(VenueSubType)
#     # Date provide programmatically, not by the DB
#     livestream = Column(String(64), nullable=True)
#     # String or stringified object
#     service_time = Column(String(250))
#     # String or stringified object
#     summary = Column(String(250), nullable=True)
#     # Pastor/Principal
#     admin_name = Column(String(250), nullable=False)
#     # Key/Value pairs
#     filters = Column(String(250), nullable=False)
#     raw_data = Column(Text)
#
#     @property
#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name
#         }
#
#
# class VenueType(Base):
#
#     __tablename__ = 'venue_type'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#
#
# class VenueSubType(Base):
#
#     __tablename__ = 'venue_sub_type'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)


# End of File ================================================================ #
engine = create_engine(Config.DATABASE)

Base.metadata.create_all(engine)