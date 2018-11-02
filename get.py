import base64
import hashlib
import json
import os
import random
import re
import secrets
import shutil
import threading
import time
import uuid
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup as bs
from flask_sqlalchemy import SQLAlchemy

from quart import (
    Quart,
    Response,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    websocket,
)

from api import ippl_api
from dbmanage import req_db

app = Quart(__name__)


def open_and_write(fn: str, mode: str = "w", data=None) -> None:
    with open(fn, mode) as f:
        f.write(data)
    return


def open_and_read(fn: str, mode: str = "r", strip: bool = True):
    with open(fn, mode) as f:
        if strip:
            data = f.read().strip()
        else:
            data = f.read()
    return data


app.secret_key = os.environ.get("db_pass_insig") or open_and_read(
    ".dbpass-insignificant"
)
try:
    dburl = os.environ.get("DATABASE_URL") or open_and_read(".dbinfo_")
except:
    raise Exception(
        "No DB url specified try add it to the environment or \
        create a .dbinfo_ file with the url"
    )
app.config["SQLALCHEMY_DATABASE_URI"] = dburl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/66.0.3343.3 Safari/537.36"


def get_all_results(req_if_not_heroku=False, number=0, shuffle=True, url=None):
    db_cache_file = os.path.join(app.root_path, ".db-cache--all")
    jsdata = __data__ = []
    data = None
    if os.path.isfile(db_cache_file):
        _data = open_and_read(db_cache_file)
        try:
            data = json.loads(_data).get("data").get("movies")
            __data__ = data
        except Exception as e:
            print(e)
    elif is_heroku(str(url)) or not is_heroku(str(url)) and req_if_not_heroku:
        _data = movieData.query.all()
        for url in _data:
            jsdata.append(
                {
                    "movie": url.moviedisplay,
                    "id": url.mid,
                    "thumb": url.thumb,
                    "moviename": url.movie,
                }
            )
        _meta = json.dumps({"stamp": time.time(), "data": {"movies": jsdata}})
        open_and_write(db_cache_file, "w", _meta)
        __data__ = jsdata
    else:
        return []
    if number:
        return random.choices(__data__, k=number)
    if shuffle:
        random.shuffle(__data__)
        return __data__


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


scripts_dir = os.path.join(app.root_path, "static", "dist")
if not os.path.isdir(scripts_dir):
    os.mkdir(scripts_dir)


def resolve_local_url(url):
    # all static assets are location in /static folder..so we dont care about urls like "./"
    if url.startswith("/"):
        return url
    elif url.startswith("."):
        url = url.lstrip(".")
    if url.startswith("static"):
        return "/" + url
    else:
        return url


def parse_local_assets(html):
    soup = bs(html, "html.parser")
    assets = soup.find_all(
        lambda x: (
            x.name == "script"
            and resolve_local_url(x.attrs.get("src", "")).startswith("/")
        )
        or (
            x.name == "link"
            and resolve_local_url(x.attrs.get("href", "")).startswith("/")
            and "stylesheet" in x.attrs.get("rel", "")
        )  # Relative urls
    )
    for data in assets:
        ftype = data.name
        attr, ext = ("src", ".js") if ftype == "script" else ("href", ".css")
        src = resolve_local_url(data.attrs.get(attr))
        print(f"Parsing asset->{src}")
        if src.startswith("/"):
            src = src[1:]
        _file = os.path.join(app.root_path, src)
        checksum = checksum_f(_file)
        name = checksum + ext
        location = os.path.join("static", "dist", name)
        if os.path.isfile(os.path.join(app.root_path, location)):
            print("No change in file..skipping")
        else:
            shutil.copyfile(_file, os.path.join(app.root_path, location))
        data.attrs[attr] = f"/{location}"
    return str(soup)


def checksum_f(filename, meth="sha256"):
    foo = getattr(hashlib, meth)()
    _bytes = 0
    total = os.path.getsize(filename)
    with open(filename, "rb") as f:
        while _bytes <= total:
            f.seek(_bytes)
            chunk = f.read(1024 * 4)
            foo.update(chunk)
            _bytes += 1024 * 4
    return foo.hexdigest()


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
    ) and ("herokuapp" in parsedurl or "ws://app_server/" in url)


class DataLytics(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    actions = db.Column(db.PickleType)
    _type = db.Column(db.String(100))

    def __init__(self, _type, act):
        self.actions = act
        self._type = _type

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


@app.route("/submit/report/", methods=["POST"])
async def parse_report():
    try:
        _mid = await request.form
        mid = _mid["id"]
        col = deadLinks(mid)
        db.session.add(col)
        db.session.commit()
        return "Response recorded.Thank You for your help!"
    except Exception as e:
        print(e)
        return "An unknown error occured during processing your request"
    # raise e


@app.route("/robots.txt")
async def check__():
    return await send_from_directory(
        os.path.join(app.root_path, "static"), "robots.txt"
    )


@app.route("/")
async def index():
    if session.get("req-data"):
        d = "Thanks for helping us out!"
    else:
        d = " "

    return parse_local_assets(await render_template("index.html", msg=d))


@app.route("/i/rec/")
async def recommend():
    data = get_all_results(False, number=5, shuffle=False, url=request.url)
    rec = json.dumps({"recommendations": data})
    return Response(rec, content_type="application/octet-stream")


@app.route("/favicon.ico")
async def send_fav():
    return await send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico"
    )


@app.route("/report")
async def report_dead():
    m_id = request.args.get("id")
    if m_id is None:
        return "No movie id specified"
    meta_ = movieData.query.filter_by(mid=m_id).first()
    if meta_ is None:
        return "No movie associated with given id"
    thumb = meta_.thumb
    title = meta_.moviedisplay
    return parse_local_assets(
        await render_template("link-report.html", m_id=m_id, title=title, thumb=thumb)
    )


@app.route("/search")
async def send_m():
    if request.args.get("q") is None or not re.sub(r"[^\w]", "", request.args.get("q")):
        return "Specify a term!"
    return parse_local_assets(
        await render_template("movies.html", q=request.args.get("q"))
    )


@app.route("/help-us/")
async def ask_get():
    return parse_local_assets(await render_template("help.html"))


@app.websocket("/suggestqueries")
async def socket_conn():
    start_time = time.time()
    while 1:
        query = await websocket.receive()
        if (time.time() - start_time) >= 300:
            print("E")
            await websocket.send(
                json.dumps(
                    {
                        "data": [
                            {
                                "timeout": True,
                                "movie": "Please Refresh Your Browser..connection timed out",
                                "id": "_",
                                "thumbnail": "no",
                            }
                        ]
                    }
                )
            )
            return
        json_data = {"data": []}
        names = get_all_results(req_if_not_heroku=False, url=websocket.url)
        json_data["data"] = [
            s
            for s in names
            if re.search(r".*?%s" % (re.escape(query)), s["movie"], re.IGNORECASE)
        ]
        if len(json_data["data"]) == 0:
            await websocket.send(json.dumps({"no-res": True}))
        else:
            json_data["data"].sort(key=sort_dict)
            await websocket.send(json.dumps({**json_data, "cached": "undefined"}))


def sort_dict(el, key="movie"):
    return el.get(key)


@app.route("/db-manage/parse-requests/", methods=["POST"])
async def get_s():
    _form = await request.form
    movie = _form.get("movie")
    if not re.sub(r"\s", "", movie):
        print("No movie Given")
        return "Please mention the movie"
    url = _form.get("url")
    data = (movie, url)
    a = req_db(data)
    print(a)
    return redirect("/", 301)


@app.route("/googlef06ee521abc7bdf8.html")
async def google_():
    return "google-site-verification: googlef06ee521abc7bdf8.html"


def movie_list_sort(md):
    return md.movie


@app.route("/data/search/", methods=["POST"])
async def serchs():
    json_data = {}
    json_data["movies"] = []
    _form = await request.form
    q = re.sub(r"[^\w]", "", _form["q"]).lower()
    urls = movieData.query.filter(movieData.movie.op("~")(r"(?s).*?%s" % (q))).all()
    urls.sort(key=movie_list_sort)

    for url in urls:
        json_data["movies"].append(
            {"movie": url.moviedisplay, "id": url.mid, "thumb": url.thumb}
        )
    if len(json_data["movies"]) == 0:
        return json.dumps({"no-res": True})
    return Response(json.dumps(json_data), content_type="application/json")


@app.route("/error-configs/")
async def err_configs():
    return await render_template("err.html")


@app.route("/all/")
async def all_movies():
    session["req-all"] = (generate_id() + generate_id())[:20]
    return parse_local_assets(
        await render_template("all.html", data=session["req-all"])
    )


@app.route("/fetch-token/configs/", methods=["POST"])
async def gen_conf():
    _data = await request.form
    data = _data["data"]
    rns = _data["rns"]
    if data != session["req-all"]:
        return "lol"
    session["req-all"] = (generate_id() + rns + generate_id())[:20]
    return Response(
        json.dumps({"id": session["req-all"], "rns": rns}),
        content_type="application/json",
    )


@app.route("/data/specs/", methods=["POST"])
async def get_all():
    json_data = {}
    _forms = await request.form
    forms = _forms["q"]
    json_data["movies"] = []
    if session["req-all"] != forms:
        return "!cool"
    movs = get_all_results(shuffle=True, url=request.url)
    json_data["movies"] = movs
    res = await make_response(json.dumps(json_data))
    res.headers["Content-Type"] = "application/json"
    return res


@app.route("/fetch-token/links/post/", methods=["POST"])
async def s_confs():
    _data = await request.form
    data = _data["data"]
    if data != session["req-all"]:
        return "No"
    session["req-all"] = (generate_id() + generate_id())[:20]
    return Response(
        json.dumps({"id": session["req-all"]}), content_type="application/json"
    )


@app.route("/movie/<mid>/<mdata>/")
async def send_movie(mid, mdata):
    if mid is None:
        return "Nope"
    session["req_nonce"] = generate_id()
    if os.path.isdir(".player-cache"):
        if os.path.isfile(os.path.join(".player-cache", mid + ".json")):
            with open(os.path.join(".player-cache", mid + ".json"), "r") as f:
                try:
                    data = json.loads(f.read())
                    res = await make_response(
                        parse_local_assets(
                            await render_template(
                                "player.html",
                                nonce=session["req_nonce"],
                                movie=data["movie_name"],
                                og_url=request.url,
                                og_image=data["thumbnail"],
                            )
                        )
                    )
                    res.headers["X-Sent-Cached"] = str(True)
                    print("Sending Cached Data")
                    return res
                except:
                    pass
    else:
        os.mkdir(".player-cache")
    meta_ = movieData.query.filter_by(mid=mid).first()
    if meta_ is None:
        return "No movie associated with given id"
    movie_name = meta_.moviedisplay
    thumbnail = meta_.thumb
    with open(os.path.join(".player-cache", mid + ".json"), "w") as f:
        data_js = {
            "movie_name": movie_name,
            "thumbnail": thumbnail,
            "url": meta_.url,
            "alt1": meta_.alt1,
            "alt2": meta_.alt2,
        }
        f.write(json.dumps(data_js))
    res = await make_response(
        parse_local_assets(
            await render_template(
                "player.html",
                nonce=session["req_nonce"],
                movie=movie_name,
                og_url=request.url,
                og_image=thumbnail,
            )
        )
    )
    res.headers["X-Sent-Cached"] = str(False)
    return res


@app.route("/data-parser/plugins/player/", methods=["POST"])
async def plugin():
    _mid = await request.form
    mid = _mid["id"]
    if _mid["nonce"] != session["req_nonce"]:
        return "Lol"
    nonce = generate_id()
    session["req_nonce"] = nonce
    if os.path.isdir(".player-cache"):
        if os.path.isfile(os.path.join(".player-cache", mid + ".json")):
            with open(os.path.join(".player-cache", mid + ".json"), "r") as f:
                try:
                    data = json.loads(f.read())
                    json_data = {
                        "url": data["url"],
                        "alt1": data["alt1"],
                        "alt2": data["alt2"],
                    }
                    res = await make_response(json.dumps(json_data))
                    res.headers["Content-Type"] = "application/json"
                    res.headers["X-Sent-Cached"] = str(True)
                    print("Sending Cached Data")
                    return res
                except:
                    pass
    else:
        os.mkdir(".player-cache")
    data = movieData.query.filter_by(mid=mid).first()
    common_ = {"url": data.url, "alt1": data.alt1, "alt2": data.alt2}
    json_data = json.dumps(
        {**common_, "movie_name": data.movie_display, "thumbnail": data.thumb}
    )
    with open(os.path.join(".player-cache", mid + ".json"), "w") as f:
        f.write(json_data)
    res = await make_response(json_data)
    res.headers["X-Sent-Cached"] = str(False)
    res.headers["Content-Type"] = "application/json"
    return res


@app.route("/no-result/")
async def b404():
    return await render_template("no-result.html")


@app.route("/sec/add/", methods=["POST"])
async def add_():
    try:
        _data = await request.form
        data = _data["data"]
        if _data["pw"] != os.environ.get("_pass_"):
            return "No"
        data = json.loads(data)
        col = movieData(*data["lists"])
        db.session.add(col)
        db.session.commit()
        return str(col)
    except:
        return "Malformed Input"


@app.route("/media/add/")
async def add_show():
    return parse_local_assets(await render_template("shows-add.html"))


@app.route("/media/add-shows/fetch/")
async def search_shows():
    show = request.args.get("s")
    print(show)
    return Response(ippl_api.main_(term=show), content_type="application/json")


@app.route("/add/tv-show/lookup")
async def add_show_lookup():
    _show_url = request.args.get("s")
    title = request.args.get("t", "")
    q = re.sub(r"([^\w]|_)", "", title).lower()
    urls = movieData.query.filter(movieData.movie.op("~")(r"(?s).*?%s" % (q))).all()
    if len(urls) > 0:
        return (
            "We already have a show with similar name..to prevent multiple copies of the same show..please request this show to be manually added",
            403,
        )
    thread = threading.Thread(target=ippl_api.get_, args=(_show_url, title))
    thread.start()
    return parse_local_assets(
        await render_template("shows_add_evt.html", show_url=_show_url, show=title)
    )


@app.route("/out/")
async def redir():
    site = session.get("site-select")
    url = request.args.get("url")
    if url.startswith("//"):
        url = "https:" + url
    return (
        parse_local_assets(await render_template("sites.html", url=url, site=site)),
        300,
    )


@app.route("/admin/", methods=["POST", "GET"])
async def randomstuff():
    pw = app.secret_key
    if request.method == "GET":
        return parse_local_assets(await render_template("admin.html"))
    else:
        if not is_heroku(request.url):
            print("Local")
            session["admin-auth"] = True
            resp = 1
        else:
            if session.get("admin-auth"):
                return Response(json.dumps({"response": -1}))
            form = await request.form
            _pass = form["pass"]
            print(_pass, pw)
            session["admin-auth"] = _pass == pw
            if not session["admin-auth"]:
                resp = "0"
            else:
                resp = "1"
    return Response(json.dumps({"response": resp}), content_type="application/json")


@app.route("/admin/get-data/", methods=["POST"])
async def see_data():
    if not session.get("admin-auth"):
        return Response(json.dumps({}))
    _ = ("search", "moviewatch", "recommend", "movieclick")
    form = await request.form
    _type_ = form["type"].lower()
    _filter = [s.actions for s in DataLytics.query.filter_by(_type=_type_).all()]
    data = {"result": _filter}
    return Response(json.dumps(data), content_type="application/json")


@app.route("/collect/", methods=["POST", "GET"])
async def collect():
    if request.method == "POST":
        _data = await request.data
        data = json.loads(_data.decode())
    else:
        data = dict(request.args)
    if not is_heroku(request.url):
        print("Local Env")
        print(data)
        return ""
    col = DataLytics(data["type"].lower(), data["main"])
    db.session.add(col)
    db.session.commit()
    return ""


@app.route("/beacon-test", methods=["POST"])
async def bcontest():
    await request.data
    return ""


@app.route("/set-downloader/")
async def set_dl():
    session["site-select"] = request.args.get("dl")
    return redirect(session["site-select"], status_code=301)


# for heroku nginx
open("/tmp/app-initialized", "w").close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", use_reloader=True)
