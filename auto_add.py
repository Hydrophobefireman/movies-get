import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
import ippl


def main_(term):
    url = "https://www2.solarmoviesc.com/search/{}.html".format(quote(term))
    ua = "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US) AppleWebKit/604.1.38 (KHTML, like Gecko) Chrome/68.0.3325.162"
    print("[debug]Fetching:\n", url)
    basic_headers = {
        "User-Agent": ua,
        "Upgrade-Insecure-Requests": "1",
        "dnt": '1',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    sess = requests.Session()
    htm = sess.get(url, headers=basic_headers, allow_redirects=True)
    page = htm.text
    soup = bs(page, 'html.parser')
    atags = soup.find_all(attrs={"data-jtip": True})
    for tag in atags:
        u = tag.attrs.get("href")
        if u:
            yn=input("Should I add:",u)
            print('[info]Adding:',u)
            print(ippl.get_(u, True))


if __name__ == "__main__":
    print(main_(input("Enter The Term:")))
