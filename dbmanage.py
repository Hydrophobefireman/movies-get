import psycopg2
from flask_sqlalchemy import SQLAlchemy
import sys


def add_to_db(data, dbInst=None, movieDataInst=None):
    if not dbInst or movieDataInst:
        pass
        # from get import db as dbInst, movieData as movieDataInst
    assert isinstance(data, tuple) and len(data) == 6
    url = data[1]
    if movieDataInst.query.filter_by(url=url).first() is not None:
        raise Exception("Added Already")
    col = movieDataInst(*data)
    dbInst.session.add(col)
    dbInst.session.commit()
    return col


def req_db(data):
    from get import db, movieRequests

    assert isinstance(data, tuple) and len(data) == 2
    col = movieRequests(*data)
    db.session.add(col)
    db.session.commit()
    return col

