
from io import BytesIO
from zipfile import ZipFile
import requests

# or: requests.get(url).content


def to_text(url):
    resp = requests.get(url)
    zipfile = ZipFile(BytesIO(resp.content))
    fn = [i for i in zipfile.namelist() if i.endswith(".srt")][0]
    with zipfile.open(fn) as f:
        return f.read()