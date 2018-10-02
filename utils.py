import re
from flask_sqlalchemy import sqlalchemy


def sort_dict(el, key="movie"):
    return el.get(key)


def movie_list_sort(md):
    return md.movie


def open_and_read(fn: str, mode: str = "r") -> str:
    with open(fn, mode) as f:
        return f.read().strip()


class movieData(db.Model):
    mid = db.Column(db.String, primary_key=True)
    movie = db.Column(db.String(100))
    moviedisplay = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    alt1 = db.Column(db.String(1000))
    alt2 = db.Column(db.String(1000))
    thumb = db.Column(db.String(1000))

    def __init__(self, movie, url, alt1, alt2, thumb):
        self.mid = generate_id()
        self.movie = re.sub(r"\s", "", movie).lower()
        self.moviedisplay = movie
        self.url = str(url).replace("http://", "https://")
        self.alt1 = str(alt1).replace("http://", "https://")
        self.alt2 = str(alt2).replace("http://", "https://")
        self.thumb = thumb

    def __repr__(self):
        return "<Name %r>" % self.movie


def generate_id() -> str:
    lst_ = secrets.token_urlsafe()
    return lst_[: gen_rn()]


def gen_rn():
    # when randint was 5..we got 3 duplicates in every 1 million entries..
    return random.randint(10, 17)


def is_heroku(url):
    parsedurl = urlparse(url).netloc
    return (
        "127.0.0.1" not in parsedurl
        or "localhost" not in parsedurl
        or "192.168." not in parsedurl
    ) and "herokuapp" in parsedurl


class DataLytics(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    actions = db.Column(db.PickleType)

    def __init__(self, act):
        self.actions = act

    def __repr__(self):
        return f"<DATA-ID:{self.idx}>"


class movieRequests(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(100))
    url = db.Column(db.String(1000))

    def __init__(self, movie, url=None):
        self.movie = movie
        self.url = url

    def __repr__(self):
        return "<Name %r>" % self.movie


class deadLinks(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, movie_id, name=None):
        self.movieid = movie_id
        self.name = name

    def __repr__(self):
        return "<Name %r>" % self.movieid

