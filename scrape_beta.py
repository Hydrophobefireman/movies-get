import re
import json
import requests
from bs4 import BeautifulSoup as bs

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.3 Safari/537.36"


def scrape(url):
    UserWarning(
        "Some Go Movies url need a /watching.html in the end. Remember to add it if needed")
    req = requests.get(url, headers={"User-Agent": USER_AGENT})
    page = req.text
    soup = bs(page, 'html.parser')
    content_div = soup.find(
        attrs={"id": 'les-content'}) or soup.find(attrs={"class": 'les-content'})
    if content_div:
        data = les_content_parser(content_div)
    else:
        url = re.search(r"var\s*locations)\s?=\s?.*?(?<=;)",
                        url, re.IGNORECASE)
        if url:
            return [url.group()]
        return try_ipplayer_search(page)


def les_content_parser(div):
    # Find all urls
    reg = r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
    urls = re.findall(reg, str(div))
    valid_urls = [s for s in urls if urlcheck(s)]
    if valid_urls:
        return valid_urls
    else:
        return 0


def urlcheck(url):
    if re.search(r"(https?:)?//.*\.?((docs|drive)\.google.com)|video\.google\.com", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?(photos\.google|photos\.app\.goo\.gl)", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?estream", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?vidzi\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?yourupload\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?dailymotion\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?watcheng\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?instag\.?ram\.?", url) is not None:
        return True
    if re.search(r"(https?:)?//.*\.?rapidvideo\.", url, re.IGNORECASE) is not None:
        return True
    if re.search(r"https?://.*?oload|https?://openload|https?://.*?daclips|https?://.*?thevideo|https?://.*?vev.io|https?://.*?streamango|https?://.*?streamago|https?://.*?streamcloud", url, re.IGNORECASE) is not None:
        return True
    else:
        return False
