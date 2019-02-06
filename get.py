import base64
import json
import os
import random
import re
import secrets
import threading
import time
from typing import Optional
from urllib.parse import urlparse

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

import api.ippl_api
from dbmanage import req_db
from set_env import set_env_vars

set_env_vars()

app = Quart(__name__)
if not os.path.isdir(".player-cache"):
    os.mkdir(".player-cache")


def open_and_write(fn: str, mode: str = "w", data=None) -> None:
    with open(fn, mode) as f:
        f.write(data)
    return


def open_and_read(fn: str, mode: str = "r", strip: bool = True):
    if not os.path.isfile(fn):
        return None
    with open(fn, mode) as f:
        if strip:
            data = f.read().strip()
        else:
            data = f.read()
    return data


app.secret_key = os.environ.get("db_pass_insig")
try:
    dburl = os.environ.get("DATABASE_URL")
except:
    raise Exception("No DB url specified try add it to the environment")
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
    # pylint: disable=E1101
    mid = db.Column(db.String, primary_key=True)
    movie = db.Column(db.String(100))
    moviedisplay = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    alt1 = db.Column(db.String(1000))
    alt2 = db.Column(db.String(1000))
    thumb = db.Column(db.String(1000))
    subs = db.Column(db.LargeBinary)
    # pylint: enable=E1101
    def __init__(self, movie, url, alt1, alt2, thumb, subs=b""):
        self.mid = generate_id()
        self.movie = re.sub(r"\s", "", movie).lower()
        self.moviedisplay = movie
        self.url = str(url).replace("http://", "https://")
        self.alt1 = str(alt1).replace("http://", "https://")
        self.alt2 = str(alt2).replace("http://", "https://")
        self.subs = subs
        self.thumb = thumb

    def __repr__(self):
        return "<Name %r>" % self.movie


def generate_id(n=None) -> str:
    lst_ = secrets.token_urlsafe(n)
    return lst_[: n or gen_rn()]


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
    # pylint: disable=E1101
    idx = db.Column(db.Integer, primary_key=True)
    actions = db.Column(db.PickleType)
    _type = db.Column(db.String(100))
    # pylint: enable=E1101

    def __init__(self, _type, act):
        self.actions = act
        self._type = _type

    def __repr__(self):
        return f"<DATA-ID:{self.idx}>"


class movieRequests(db.Model):
    # pylint: disable=E1101
    r_id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    # pylint: enable=E1101
    def __init__(self, movie, url=None):
        self.movie = movie
        self.url = url

    def __repr__(self):
        return "<Name %r>" % self.movie


class deadLinks(db.Model):
    # pylint: disable=E1101
    r_id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # pylint: enable=E1101

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
        # pylint: disable=E1101
        db.session.add(col)
        db.session.commit()
        # pylint: enable=E1101
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


@app.route("/api/gen_204/")
async def _start_frontend():
    return Response("", status=204)


@app.errorhandler(404)
async def err(err):
    if is_heroku(request.url):
        return redirect("https://movies.pycode.tk")
    return "404"


@app.route("/")
async def index():
    if "localhost" not in request.headers.get("origin", ""):
        return redirect("https://movies.pycode.tk")
    return "ok"


@app.route("/i/rec/")
async def recommend():
    data = get_all_results(False, number=5, shuffle=False, url=request.url)
    rec = json.dumps({"recommendations": data})
    return Response(rec, content_type="application/json")


@app.after_request
async def resp_headers(resp):
    if "localhost" in request.headers.get("origin", ""):
        resp.headers["access-control-allow-origin"] = request.headers["origin"]
    else:
        resp.headers["access-control-allow-origin"] = "https://movies.pycode.tk"
    resp.headers["access-control-allow-credentials"] = "true"
    return resp


@app.route("/favicon.ico")
async def send_fav():
    return await send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico"
    )


@app.websocket("/suggestqueries")
async def socket_conn():
    while 1:
        query = await websocket.receive()
        if query == "ping":
            await websocket.send("pong")
        else:
            json_data = {"data": []}
            names = get_all_results(req_if_not_heroku=False, url=websocket.url)
            json_data["data"] = [
                s
                for s in names
                if re.search(
                    (re.sub(r"[^\w]", "", query)), s["moviename"], re.IGNORECASE
                )
            ]
            if len(json_data["data"]) == 0:
                await websocket.send(json.dumps({"no-res": True}))
            else:
                json_data["data"].sort(key=sort_dict)
                await websocket.send(json.dumps({**json_data, "cached": "undefined"}))


def sort_dict(el, key="movie"):
    return el.get(key)


@app.route("/api/request/", methods=["POST"])
async def api_req_m():
    _form = await request.form
    movie = _form.get("movie")
    if not re.sub(r"\s", "", movie):
        print("No movie Given")
        return "NO"
    url = _form.get("url")
    data = (movie, url)
    a = req_db(data)
    print(a)
    return "OK"


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


@app.route("/api/all/")
async def get_token():
    token = (generate_id() + generate_id())[:20]
    session["req-all"] = token
    return Response(json.dumps({"token": token}), content_type="application/json")


@app.route("/fetch-token/configs/", methods=["POST"])
async def gen_conf():
    _data = await request.form
    data = _data["data"]
    rns = _data["rns"]
    if data != session.get("req-all"):
        return "lol"
    session.pop("req-all")
    session["fetch-token"] = (generate_id() + rns + generate_id())[:20]
    return Response(
        json.dumps({"id": session["fetch-token"], "rns": rns}),
        content_type="application/json",
    )


@app.route("/data/specs/", methods=["POST"])
async def get_all():
    json_data = {}
    _forms = await request.form
    forms = _forms["q"]
    json_data["movies"] = []
    if session.get("data-specs") != forms:
        return "!cool"
    session.pop("data-specs")
    movs = get_all_results(shuffle=True, url=request.url)
    json_data["movies"] = movs
    res = await make_response(json.dumps(json_data))
    res.headers["Content-Type"] = "application/json"
    return res


@app.route("/fetch-token/links/post/", methods=["POST"])
async def s_confs():
    _data = await request.form
    data = _data["data"]
    if data != session.get("fetch-token"):
        return "No"
    session.pop("fetch-token")
    session["data-specs"] = generate_id(30)
    return Response(
        json.dumps({"id": session["data-specs"]}), content_type="application/json"
    )


@app.route("/api/movie/", methods=["POST"])
async def _frontend_movie():
    ct = "application/json"
    data: str

    form = await request.form
    idx: Optional[str] = form.get("id")
    if not idx:
        return Response(
            json.dumps({"error": "no id provided"}), content_type=ct, status=400
        )

    _data: Optional[dict] = _get_data_from_player_cache(idx)
    if not _data:
        meta_ = movieData.query.filter_by(mid=idx).first()
        if not meta_:
            return Response(json.dumps({"error": "_nomovie_"}), content_type=ct)
        movie_name: str = meta_.moviedisplay
        thumbnail: str = meta_.thumb
        data = json.dumps(
            {
                "movie_name": movie_name,
                "thumbnail": thumbnail,
                "url": meta_.url,
                "alt1": meta_.alt1,
                "alt2": meta_.alt2,
            }
        )

        open_and_write(os.path.join(".player-cache", f"{idx}.json"), "w", data)
    else:
        data = json.dumps(_data)
    return Response(data, content_type=ct)


def _get_data_from_player_cache(mid: str) -> dict:
    fp = os.path.join(".player-cache", f"{mid}.json")
    f = open_and_read(fp)
    if not f:
        return None
    try:
        data = json.loads(f)
        return {
            "movie_name": data["movie_name"],
            "thumbnail": data["thumbnail"],
            "url": data["url"],
            "alt1": data["alt1"],
            "alt2": data["alt2"],
        }
    except:
        return None


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


@app.route("/media/add-shows/fetch/")
async def search_shows():
    show = request.args.get("s")
    print(show)
    return Response(ippl_api.main_(term=show), content_type="application/json")


@app.route("/api/add/tv-show/lookup")
async def frontend_add_show_lookup():
    _show_url = request.args.get("s")
    title = request.args.get("t", "")
    q = re.sub(r"([^\w]|_)", "", title).lower()
    urls = movieData.query.filter(movieData.movie.op("~")(r"(?s).*?%s" % (q))).all()
    if len(urls) > 0:
        return "We already have a movie with similar name..to prevent multiple copies of the same movie..please request this show to be manually added"
    thread = threading.Thread(target=ippl_api.get_, args=(_show_url, title))
    thread.start()
    return "OK"


@app.route("/api/out/")
async def _frontend_redir():
    site = session.get("site-select")
    url = request.args.get("url")
    if url.startswith("//"):
        url = "https:" + url
    return Response(json.dumps({"site": site, "url": url}))


@app.route("/collect/", methods=["POST", "GET"])
async def collect():
    return ""


@app.route("/beacon-test", methods=["POST"])
async def bcontest():
    return ""


@app.route("/set-downloader/")
async def set_dl():
    session["site-select"] = request.args.get("dl")
    return redirect(session["site-select"], status_code=301)


# for heroku nginx
@app.before_serving
def open_to_nginx():
    open("/tmp/app-initialized", "w").close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", use_reloader=True)
