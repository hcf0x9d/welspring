#!/usr/bin/python3

# Configuration ============================================================== #
import random
import string

from district_portal import app
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

Base = declarative_base()

# Generating a secret key for our OAuth process
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in range(32))


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(250))
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def varify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    # @property
    # def serialize(self):
    #     """Return object data in easily serializeable format"""
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'email': self.email,
    #         'picture': self.picture
    #     }


class Category(Base):

    __tablename__ = 'category'

    name = Column(String(80), nullable=False)
    icon = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    slug = Column(String(80), nullable=False)

    # @property
    # def serialize(self):
    #     """For developing an API endpoint
    #
    #     Returns the item object for an API endpoint
    #     """
    #
    #     # TODO: Fill out the endpoint information for the Category (api)
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #     }


class Item(Base):

    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    slug = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# End of File ================================================================ #
engine = create_engine(app.config['DATABASE'])

Base.metadata.create_all(engine)
