import json
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs


def check_for_stream_sites(url, ua):
    s_sites = ["coolseries.video", "watchseries.",
               "watch-series", "tvzion", "putlocker"]
    data = False
    if any(a in url for a in s_sites):
        if re.search(r"https?://.*?coolseries\.", url) is not None:
            data = cool_series(url, ua)
        if re.search(r"https?://.*watch.?series", url) is not None:
            data = watchseries(url, ua)
        if re.search(r"https?://.*?tvzion", url) is not None:
            data = tvzion(url, ua)
        if re.search(r"https?://.*?putlocker", url) is not None:
            print("try")
            data = putlocker(url, ua)
        return data
    else:
        # if down.urlcheck(url)[0]:  # Not a streaming site
        return False


def putlocker(url, ua):
    source = requests.get(url, headers={"User-Agent": ua}).text
    # too many rip off sites..gotta support some of em

    def searches(url, source):
        try:
            g = re.findall(r"((?<=src:\s').*?(?=\',))", source)
            if "embed/" in str(g):
                print(g[0])
                d = requests.get(urlparse(url).scheme+"://" +
                                 urlparse(url).netloc+g[0]).text
                url = bs(d, "html.parser").find("iframe").attrs.get('src')
                print(url)
                if url:
                    return [url]
            print("pid")
        except:
            pass
        try:
            p_id = re.findall(r"((?<=post_id\":\").*?(?=\"}))", source)[0]
            data_src = json.loads(requests.post(urlparse(url).scheme+"://"+urlparse(url).netloc + "/wp-admin/admin-ajax.php", data={
                "action": "get_oload_gs", "post_id": p_id}).text).get("src")
            return [data_src]
        except Exception as e:
            print(e)
            pass
        try:
            res = [s for s in re.findall(
                r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', source) if "http" in s]
            print(len(res))
            data = [s for s in res if down.urlcheck(s)[0]]
            print(data)
            return data
        except Exception as e:
            return False
        # looks terrible but there are a few 100 putlocker domains around this supports most of them except one
    res = searches(url, source)
    if not res:
        try:
            parsed_url = urlparse(url)
            base_url_check = parsed_url.scheme+"://"+parsed_url.netloc+"/tmp_chk.php"
            requests.post(base_url_check, data={"tst": parsed_url.netloc})
            source = requests.post(url, data={"tmp_chk": 1}).text
            res = searches(url, source)
            return res
        except Exception as e:
            print(e)
            return False
    return res


def tvzion(url, ua):
    _test = [
        'https://www2.tvzion.com/watch-the-office-season-3-episode-14-s03e14-online3-free-v1-2316']
    source = requests.get(url, headers={"User-Agent": ua}).text
    source = re.sub(r"\s", '', source)
    data = []
    videoreg = r"((?<=rel=\"video_src\"href=\").*?(?=\"))"
    video = re.findall(videoreg, source)
    sess = requests.Session()
    video = sess.get(
        video[0], headers={"User-Agent": ua, "Referer": url}, allow_redirects=True).url
    if any(a in video for a in down.working_sites):
        data.append(video)
        return data
    else:
        return False


def watchseries(url, ua):  # general extractor
    source = requests.get(url, headers={"User-Agent": ua}).text
    urls = re.findall(r"https?://.*?(?=\")", source)
    data = []
    for u in urls:
        if "/external/" in u:
            u = get_final_url(u, ua, url)
            if u:
                data += u  # we need one list only
        elif any(a in u for a in down.working_sites):
            data.append(u)
    return data


def get_final_url(u, ua, url):
    hosts = extract_host(url)
    source = requests.get(u, headers={"User-Agent": ua, "Referer": url}).text
    urls = re.findall(
        r'(?:(?:https?|ftp)?:\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', source)
    data = []
    for u in urls:
        if extract_host(u) != hosts:
            if u.startswith("//"):
                u = "http:"+u
            if down.urlcheck(u)[0]:
                data.append(u)
    return data


def extract_host(url):
    if re.search("https?://", url) is None:
        hosts = url.split("/")[0]
    else:
        hosts = url.split("://")[1].split("/")[0]
    return hosts


def cool_series(url, ua):
    data = requests.get(url, headers={"User-Agent": ua}).text
    data = re.sub(r"[\s]", '', data)
    regex = r'((?<=<IFRAMESRC=").*?(?="\w?))'
    iframes = [s for s in re.findall(
        regex, data, re.IGNORECASE) if "http" in s and "vidfast" not in s]
    g_urls = []
    for url in iframes:
        hts = bs(requests.get(url, headers={
            "User-Agent": ua, "Referer": url, "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"}).text, "html.parser")
        iframeurl = hts.findAll("iframe")[0].attrs['src']
        if any(a in iframeurl for a in down.working_sites):
            g_urls.append(iframeurl)
    return g_urls
