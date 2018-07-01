import psycopg2
from flask_sqlalchemy import SQLAlchemy
import sys
from get import db, movieData, movieRequests


def add_to_db(data):
    assert isinstance(data, tuple) and len(data) == 5
    col = movieData(*data)
    db.session.add(col)
    db.session.commit()
    return col


def req_db(data):
    assert isinstance(data, tuple) and len(data) == 2
    col = movieRequests(*data)
    db.session.add(col)
    db.session.commit()
    return movieRequests.query.all()
