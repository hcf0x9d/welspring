#!/usr/bin/python3

# Configuration ============================================================== #
from config import Config
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
#                          BadSignature, SignatureExpired)

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


class UserType(Base):
    __tablename__ = 'user_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(250))
    password_hash = Column(String(64))
    user_type_id = Column(Integer, ForeignKey('user_type.id'), default=1)
    user_venue_type = relationship(UserType)

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(secret_key)
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         # Valid Token, but expired
    #         return None
    #     except BadSignature:
    #         # Invalid Token
    #         return None
    #     user_id = data['id']
    #     return user_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class VenueType(Base):
    __tablename__ = 'venue_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class VenueSubType(Base):
    __tablename__ = 'venue_sub_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    venue_type_link = Column(Integer, ForeignKey('venue_type.id'))
    venue_type = relationship(VenueType)


class Venue(Base):
    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True)
    google_id = Column(String(64), index=True)
    # Church or school
    slug = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    website = Column(String(250))
    # lat/lng string from google
    location = Column(String(250))
    phone = Column(String(8))
    # HTML entry with spans like Google's API
    address = Column(String(250))
    type_id = Column(Integer, ForeignKey('venue_type.id'))
    venue_type = relationship(VenueType)
    sub_type_id = Column(Integer, ForeignKey('venue_sub_type.id'))
    venue_sub_type = relationship(VenueSubType)
    # Date provide programmatically, not by the DB
    livestream = Column(String(64))
    # String or stringified object
    service_time = Column(String(250))
    # String or stringified object
    summary = Column(String(250))
    picture = Column(String(250))
    # Pastor/Principal
    admin_name = Column(String(250))
    # Key/Value pairs
    filters = Column(String(250))
    state = Column(String(250))
    active = Column(Boolean)
    raw_data = Column(Text)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'google_id': self.google_id,
            'website': self.website,
            'location': self.location,
            'phone': self.phone,
            'address': self.address,
            'type_id': self.type_id,
            'sub_type_id': self.sub_type_id,
            'livestream': self.livestream,
            'service_time': self.service_time,
            'summary': self.summary,
            'picture': self.picture,
            'admin_name': self.admin_name,
            'state': self.state
        }


# End of File ================================================================ #
engine = create_engine(Config.DATABASE)

Base.metadata.create_all(engine)
