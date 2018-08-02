import psycopg2
from flask_sqlalchemy import SQLAlchemy
import sys


def add_to_db(data):
    from get import db, movieData

    assert isinstance(data, tuple) and len(data) == 5
    url = data[1]
    if movieData.query.filter_by(url=url).first() is not None:
        raise Exception("Added Already")
    col = movieData(*data)
    db.session.add(col)
    db.session.commit()
    return col


def req_db(data):
    from get import db, movieRequests

    assert isinstance(data, tuple) and len(data) == 2
    col = movieRequests(*data)
    db.session.add(col)
    db.session.commit()
    return col
