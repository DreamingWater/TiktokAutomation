# Lenovo-"Xie Yan"
import requests
import re

from requests.exceptions import ProxyError


def request_country_info():
    # 获取本机IP地址
    res = requests.get("http://myip.ipip.net/")
    html = res.text.strip()
    match = re.search(r"来自于：(.*?)\s{2}", html)
    if match:
        country = match.group(1)
        if "北京" in country:
            return False
    return True


def judge_internet_connected():
    try:
        res = requests.get("http://myip.ipip.net/")
        html = res.text.strip()
        match = re.search(r"来自于：(.*?)\s{2}", html)
        if match:
            country = match.group(1)
            if "北京" in country or "香港" in country:
                return False
            match = re.search(r"IP：(.*?)\s{2}", html) # 获取IP地址
            return match.group(1)
        return False
    except ProxyError:
        return False
