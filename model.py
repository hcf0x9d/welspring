#!/usr/bin/python3

# Configuration ============================================================== #
from config import Config
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
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


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(250))
    password_hash = Column(String(64))


class Venue(Base):

    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True)
    google_id = Column(String(64), nullable=False, index=True)
    # Church or school
    type = Column(String(64), nullable=False, index=True)
    # Date provide programmatically, not by the DB
    livestream = Column(Boolean, nullable=True)
    # String or stringified object
    service_time = Column(String(250))
    raw_data = Column(Text)


# End of File ================================================================ #
engine = create_engine(Config.DATABASE)

Base.metadata.create_all(engine)