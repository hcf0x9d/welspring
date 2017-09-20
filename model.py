#!/usr/bin/python3

# Configuration ============================================================== #
from sqlalchemy import Column, Integer, String, Text
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


# End of File ================================================================ #
engine = create_engine('postgresql://welspring:password@localhost/welspring')

Base.metadata.create_all(engine)