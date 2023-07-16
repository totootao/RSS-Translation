import requests
from parsel import Selector

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def fetch(url: str, headers: dict=DEFAULT_HEADERS, proxies: dict=None):
    try:
        res = requests.get(url, headers=headers, proxies=proxies,verify=False)
        res.encoding = "utf-8"
        res.raise_for_status()
    except Exception as e:
        print(f'[Err] {e}')
    else:
        html = res.text
        # print(url)
        tree = Selector(text=html)
        return tree
