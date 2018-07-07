import re
import json
import requests
import ippl
from bs4 import BeautifulSoup as bs
from warnings import warn
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.3 Safari/537.36"


def scrape(url):
    warn("Some Go Movies url need a /watching.html in the end. Remember to add it if needed")
    req = requests.get(url, headers={"User-Agent": USER_AGENT})
    page = req.text
    soup = bs(page, 'html.parser')
    content_div = soup.findAll(
        attrs={"class": 'les-content'})
    if len(content_div) == 0:
        content_div = soup.findAll(attrs={"id": 'les-content'})
    dv = []
    for div in content_div:
        data = les_content_parser(div)
        if data:
            dv += data
    if dv:
        return dv
    else:
        url = re.search(r"var\s*locations\s?=\s?.*?(?<=;)",
                        url, re.IGNORECASE)
        if url:
            return [url.group()]
        urls = iframe_src_or_none(soup)
        if urls:
            return urls
        ippl_try = try_ipplayer_search(url)
        if ippl_try:
            return ippl_try


def try_ipplayer_search(url):
    try:
        return ippl.get_(url, v=True)
    except:
        return None


def les_content_parser(div):
    # Find all urls
    reg = r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
    urls = re.findall(reg, str(div))
    valid_urls = [s for s in urls if urlcheck(s)]
    if valid_urls:
        return valid_urls
    else:
        return None


def urlcheck(url):
    if re.search(r"^(https?:)?//.*\.?((docs|drive)\.google.com)|video\.google\.com", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?(photos\.google|photos\.app\.goo\.gl)", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?estream", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?vidzi\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?yourupload\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?dailymotion\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?watcheng\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?rapidvideo\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//.*\.?megadrive\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"^(https?:)?//(.{3})?\.?(oload|openload|daclips|thevideo|vev.io|streamango|streamago|streamcloud)", url, re.IGNORECASE) is not None:
        return True
    else:
        return False


def iframe_src_or_none(page):
    iframe = page.findAll("iframe", attrs={"src": True})
    data = []
    reg = r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
    for fr in iframe:
        if len(fr.attrs.get("src")) < 1:
            continue
        print("Found an Iframe url")
        f = fr.attrs['src']
        if "kizyplayer" in f:
            print("Using Kizy Player")
            if f.startswith("//"):
                f = "http:"+f
            source = requests.get(f, headers={"User-Agent": USER_AGENT}).text
            url = re.search(
                r"addiframe\(('|\")(?P<url>.*?)('|\"),", source, re.IGNORECASE)
            if url:
                url = url.group('url')
                if url.startswith("//"):
                    url = 'http:'+url
                print("Fetching:", url)
                source = requests.get(url, headers={
                    "User-Agent": USER_AGENT, "Referer": f}).text
                urls = re.findall(r"(?s)file:\s?['|\"].*?['|\"],", source)
                for r in urls:
                    data.append(re.search(reg, r).group())
                return data
    return None


if __name__ == '__main__':
    print(scrape(input("url:")))
