#!/usr/bin/python3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Base, Data

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

    def create_data_entry(self, type, date, title, subtitle, body):
        entry = Data(type=type, date=date, title=title,
                     subtitle=subtitle,
                     body=body)
        session.add(entry)
        session.commit()
        return
