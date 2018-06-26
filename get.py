import base64
import json
import os
import re
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

import streamsites as st

app = Flask(__name__)
try:
    with open(".dbinfo_", "r") as f:
        dburl = f.read()
except:  # heroku
    dburl = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = dburl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.3 Safari/537.36"


class moviedata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(100))
    url = db.Column(db.String(1000))

    def __init__(self, movie, url):
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search/")
def ble():
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
    return render_template("movies.html", data=json.dumps(ret))


@app.route("/out")
def redir():
    url = request.args.get("url")
    return redirect("http://dl-py.herokuapp.com/video?url="+url)


if __name__ == "__main__":
    app.run()
