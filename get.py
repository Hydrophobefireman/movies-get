import json
import os
import re
import uuid
from urllib.parse import quote, unquote
from htmlmin.minify import html_minify
import psycopg2
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from dbmanage import req_db
import streamsites as st

app = Flask(__name__)
app.secret_key = "S9(c#d4"
dburl = os.environ.get('DATABASE_URL')
try:
    if dburl is None:
        with open(".dbinfo_", "r") as f:
            dburl = f.read()
except FileNotFoundError:
    raise Exception(
        "No DB url specified try add it to the environment or create a .dbinfo_ file with the url")
app.config['SQLALCHEMY_DATABASE_URI'] = dburl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.3 Safari/537.36"


class movieData(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(100))
    moviedisplay = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    alt1 = db.Column(db.String(1000))
    alt2 = db.Column(db.String(1000))
    thumb = db.Column(db.String(1000))

    def __init__(self, movie, url, alt1, alt2, thumb):
        self.movie = re.sub(r"\s", "", movie).lower()
        self.moviedisplay = movie
        self.url = url.replace("http://", "https://")
        self.alt1 = alt1.replace("http://", "https://")
        self.alt2 = alt2.replace("http://", "https://")
        self.thumb = thumb

    def __repr__(self):
        return '<Name %r>' % self.movie


class movieRequests(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(100))
    url = db.Column(db.String(1000))

    def __init__(self, movie, url=None):
        self.movie = movie
        self.url = url

    def __repr__(self):
        return '<Name %r>' % self.movie


def urlcheck(url):
    print(url)
    if re.search(r"(https?:)?//.*\.?((docs|drive)\.google.com)|video\.google\.com", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"(https?:)?//.*\.?estream", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"(https?:)?//.*\.?vidzi\.", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"(https?:)?//.*\.?yourupload\.", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"(https?:)?//.*\.?watcheng\.", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"https?://.*?coolseries\.", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"https?://.*?(chillingeffects|lumendatabase)\.org", url, re.IGNORECASE) is not None:
        return True
    elif re.search(r"https?://.*?oload|https?://openload|https?://.*?daclips|https?://.*?thevideo|https?://.*?vev.io|https?://.*?streamango|https?://.*?streamago|https?://.*?streamcloud", url, re.IGNORECASE) is not None:
        return True
    else:
        return False


@app.before_request
def https():
    if request.endpoint in app.view_functions and not request.is_secure and "127.0.0.1" not in request.url and not "localhost" in request.url:
        return redirect(request.url.replace("http://", "https://"), code=301)
    if request.method == "GET" and not session.get("verified"):
        print(session.get("verified"))
        session['nonce'] = "_"+str(uuid.uuid4())
        return html_minify(render_template("verifysess.html", nonce=session['nonce'], to=request.url))


@app.route("/scr/", methods=['POST'])
def check__():
    data = request.form['jchk']
    if data != session['nonce']:
        return "no"
    session['verified'] = True
    return redirect(request.form['redir'])


@app.route("/")
def index():
    if session.get("req-data"):
        d = "Thanks for helping us out!"
    else:
        d = " "
    return html_minify(render_template("index.html", msg=d))


@app.route("/search")
def send_m():
    if request.args.get("q") is None or not re.sub(r"[^\w]", "", request.args.get("q")):
        return "Specify a term!"
    return html_minify(render_template("movies.html", q=request.args.get("q")))


@app.route("/help-us/")
def ask_get():
    return html_minify(render_template("help.html"))


@app.route("/db-manage/parse-requests/", methods=['POST'])
def get_s():
    movie = request.form.get('movie')
    if not re.sub(r"\s", "", movie):
        print("No movie Given")
        return "Please mention the movie"
    url = request.form.get('url')
    data = (movie, url)
    a = req_db(data)
    print(a)
    session['req-data'] = True
    return redirect("/", 301)


@app.route("/data/search/", methods=['POST'])
def serchs():
    json_data = {}
    json_data['movies'] = []
    q = re.sub(r"\s", "", request.form["q"]).lower()
    print(q)
    urls = movieData.query.filter(
        movieData.movie.op("~")(r"(?s).*?%s" % (q))).all()
    for url in urls:
        json_data['movies'].append(
            {"movie": url.moviedisplay, "url": url.url, "url1": url.alt1, "url2": url.alt2, "thumb": url.thumb})
    if len(json_data['movies']) == 0:
        return json.dumps({'redirect': '/no-result'})
    return json.dumps(json_data)


@app.route("/no-result/")
def b404():
    return render_template("no-result.html")


@app.route("/data/imagebin/<path:url>/")
def redirtoimg(url):
    return redirect(unquote(url), code=301)


@app.route("/search/g/")
def ble():
    raise NotImplementedError("Nah")
    q = request.args.get("q")
    q = "watch "+q
    url = "https://google.com/search?q="+quote(q)
    print(url)
    data = requests.get(url, headers={'User-Agent': USER_AGENT}).text
    print("connected")
    regex = r"((?<=href=\").*?(?=\"))"
    js_data = []
    link_list = [s for s in re.findall(regex, data) if s.startswith(
        "http") and ".google" not in s and "youtube.com/?gl=" not in s and "www.blogger.com/?tab=wj" not in s
        and ".bing" not in s and ".microsoft" not in s]
    fl = [s for s in link_list if urlcheck(s)]
    for t in fl:
        if re.search(r"https?://.*?(chillingeffects|lumendatabase)\.org", t, re.IGNORECASE) is not None:
            r = requests.get(t, headers={"User-Agent": USER_AGENT}).text
            soup = bs(r, 'html.parser')
            urls = [s.text for s in soup.find_all(
                "li", attrs={"class", "infringing_url"})]
            js_data += urls
    js_data = list(set(js_data))
    js_data = [s for s in js_data if urlcheck(s)]
    ret = []
    for url in js_data:
        sites = st.check_for_stream_sites(url, USER_AGENT)
        if sites:
            ret += sites
        else:
            ret.append(url)
    return html_minify(render_template("movies-google.html", data=json.dumps(ret)))


@app.route("/out")
def redir():
    url = request.args.get("url")
    return redirect("http://dl-py.herokuapp.com/video?url="+url)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
