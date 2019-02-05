import cloudinary.uploader

import os
from set_env import set_env_vars

set_env_vars()


def upload(imgurl):
    clapi_key = os.environ.get("key")
    clapi_secret = os.environ.get("cl_secret")
    if clapi_key is None:
        raise Exception("no key provided")
    cloudinary.config(cloud_name="proxypy", api_key=clapi_key, api_secret=clapi_secret)
    a = cloudinary.uploader.upload(imgurl, transformation={"size": "150x200"})
    return a


if __name__ == "__main__":
    data = upload(input("enter url:"))
    print("Raw Data:%s\n\n" % (data))
    print(data.get("secure_url"))
