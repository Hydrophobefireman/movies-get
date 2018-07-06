import json
import re
from time import sleep
from urllib.parse import urlparse as urlp_

import requests
from bs4 import BeautifulSoup as bs

import dbmanage
import upload


def get_(url, v=True):
    ua = "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US) AppleWebKit/604.1.38 (KHTML, like Gecko) Chrome/68.0.3325.162"
    print("[debug]Fetching:\n", url)
    basic_headers = {
        "User-Agent": ua,
        "Upgrade-Insecure-Requests": "1",
        "dnt": '1',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    sess = requests.Session()
    to_screen(["[debug]Using Standard Headers:", basic_headers], v)
    page = sess.get(url, headers=basic_headers, allow_redirects=True)
    to_screen(["[debug]Page URL:", page.url], v)
    to_screen(["[debug]Cookie Jar For %s:%s\n" %
               (page.url, dict(page.cookies))], v)
    soup = bs(page.text, "html.parser")
    url_ = page.url
    to_screen(["[debug]Adding Referer to headers"], v)
    basic_headers = {**basic_headers, "Referer": url_}
    to_screen(["[debug]Adding X-Requested-With to headers"], v)
    basic_headers = {**basic_headers, "X-Requested-With": "XMLHttpRequest"}
    parsed_url = urlp_(url_)
    host = "https://"+parsed_url.netloc+"/"
    div = soup.find(attrs={"data-id": "1"})
    to_screen(["[debug]Finding Ipplayer Configs"], v)
    if div is None:
        raise Exception("Could Not Find Ipplayer Configs")
    tags = div.findChildren(attrs={"data-film": True})
    data = []
    for t in tags:
        to_screen(["[debug]Working with the configs of", t.string], v)
        to_send = t.attrs
        to_screen(["[debug]Found Configs:", t.attrs], v)
        to_screen(["[debug]Sleeping for 2 seconds"], v)
        sleep(2)
        to_screen(["\n[debug]Making a post request"], v)
        a = sess.post(host+"ip.file/swf/plugins/ipplugins.php", headers=basic_headers, data={
                      "ipplugins": 1, "ip_film": to_send["data-film"], "ip_server": to_send["data-server"], "ip_name": to_send["data-name"], "fix": 'null'})
        b = json.loads(a.text)
        to_screen(["[debug]Sleeping for 2 seconds"], v)
        sleep(2)
        to_screen(["[debug]Recieved:", b], v)
        ret = sess.post(host+"ip.file/swf/ipplayer/ipplayer.php", cookies=page.cookies, headers=basic_headers,
                        data={"u": b["s"], "w": "100%25", "h": "500", "s": to_send["data-server"], 'n': '0'})
        res = json.loads(ret.text)
        to_screen(["[debug]Cookie Jar For %s:%s\n" %
                   (ret.url, dict(ret.cookies))], v)
        to_screen(["[debug]Recieved Data:", res], v)
        data.append(res.get("data"))
    to_screen(["\n[debug]Finding Title"], v)
    title = soup.find("input", attrs={"name": "movies_title"}).attrs["value"]
    to_screen(["[debug]Found:", title], v)
    to_screen(["[debug]Finding Thumbnail"], v)
    thumbnail = soup.find("input", attrs={"name": "phimimg"}).attrs["value"]
    to_screen(["[debug]Found", thumbnail], v)
    to_screen(["[debug]Fetching Thumbnail and uploading to cdn"], v)
    image = upload.upload(thumbnail).get("secure_url")
    to_screen(["[debug]Secure URL of Image:", image], v)
    while len(data) > 3:
        p_print(data)
        dt_n = input(
            "[info]Enter the number of the url to remove from the List:")
        data.pop(int(dt_n)-1)
    if len(data) < 3:
        nones = [None]*(3-len(data))
        data += nones
    data_dict = {"title": title, "thumbnail": image, "urls": data}
    db_m_tuple = (data_dict['title'], *
                  data_dict['urls'], data_dict['thumbnail'])
    yn = input("[info]Add to Databse:\n\n%s ?(y/n)" %
               (str(db_m_tuple))).lower()
    if yn == 'y':
        print('[info]Adding to database:')
        print(dbmanage.add_to_db(db_m_tuple))
    else:
        print("[info]Returning Values Only")
    return json.dumps(data_dict)


def p_print(el):
    for r in el:
        print("%d. %s" % (el.index(r)+1, r))


def to_screen(data, v):
    assert isinstance(data, list)
    if v:
        print(*data)
    else:
        return


if __name__ == "__main__":
    url = input("Enter URL:")
    verb = input("Enter Verbosity Level(v/s)[v-verbose;s-silent]").lower()
    if verb == 'v':
        verb = True
    else:
        verb = False
        print("[info]Verbosity set to silent")
    get_(url, verb)
