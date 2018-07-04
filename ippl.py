import json
import re
from time import sleep
from urllib.parse import urlparse as urlp_

import requests
from bs4 import BeautifulSoup as bs

import dbmanage
import upload


def get_(url, v=True):
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3477.0 Safari/537.36"
    print("[debug]Fetching:\n", url)
    basic_headers = {
        "User-Agent": ua,
        "Upgrade-Insecure-Requests": "1",
        "dnt": '1',
        'save-data': 'on',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }
    sess = requests.Session()
    print("[debug]Using Standard Headers:", basic_headers)
    page = sess.get(url, headers=basic_headers, allow_redirects=True)
    print("[debug]Page URL:", page.url)
    print("[debug]Cookie Jar For %s:%s\n" %
          (page.url, str(dict(page.cookies))))
    soup = bs(page.text, "html.parser")
    url_ = page.url
    print("[debug]Adding Referer to headers")
    basic_headers = {**basic_headers, "Referer": url_}
    parsed_url = urlp_(url_)
    host = "https://"+parsed_url.netloc+"/"
    div = soup.find(attrs={"data-id": "1"})
    print("[debug]Finding Ipplayer Configs")
    if div is None:
        raise Exception("Could Not Find Ipplayer Configs")
    tags = div.findChildren(attrs={"data-film": True})
    data = []
    for t in tags:
        print("[debug]Working with the configs of", t.string)
        to_send = t.attrs
        print("[debug]Found Configs:", t.attrs)
        print("[debug]Sleeping for 2 seconds")
        sleep(2)
        print("\n[debug]Making a post request")
        a = sess.post(host+"ip.file/swf/plugins/ipplugins.php", headers=basic_headers, data={
                      "ipplugins": 1, "ip_film": to_send["data-film"], "ip_server": to_send["data-server"], "ip_name": to_send["data-name"], "fix": 'null'})
        b = json.loads(a.text)
        print("[debug]Sleeping for 2 seconds")
        sleep(2)
        print("[debug]Recieved:", b)
        ret = sess.post(host+"ip.file/swf/ipplayer/ipplayer.php", cookies=page.cookies, headers=basic_headers,
                        data={"u": b["s"], "w": "100%25", "h": "500", "s": to_send["data-server"], 'n': '0'})
        res = json.loads(ret.text)
        print("[debug]Cookie Jar For %s:%s\n" %
              (ret.url, str(dict(ret.cookies))))
        print("[debug]Recieved Data:", res)
        data.append(res.get("data").replace("http://", "https://"))
    print("\n[debug]Finding Title")
    title = soup.find("input", attrs={"name": "movies_title"}).attrs["value"]
    print("[debug]Found:", title)
    print("[debug]Finding Thumbnail")
    thumbnail = soup.find("input", attrs={"name": "phimimg"}).attrs["value"]
    print("[debug]Found", thumbnail)
    print("[debug]Fetching Thumbnail and uploading to cdn")
    image = upload.upload(thumbnail).get("secure_url")
    print("[debug]Secure URL of Image:", image)
    data_dict = {"title": title, "thumbnail": image, "urls": data}
    db_m_tuple = (data_dict['title'], *
                  data_dict['urls'], data_dict['thumbnail'])
    yn = input("[info]Add to Databse:\n\n%s ?(y/n)" %
               (str(db_m_tuple))).lower()
    if yn == 'y':
        print('[debug]Adding to database:', db_m_tuple)
        print(dbmanage.add_to_db(db_m_tuple))
    else:
        print("[debug]Returning Values Only")
    return json.dumps(data_dict)


if __name__ == "__main__":
    print(get_(input("Enter URL:")))
