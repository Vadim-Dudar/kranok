import requests
from bs4 import BeautifulSoup as bs


class Parce():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def html(self, url,params=None, headers=heasers):
        r = requests.get(url, params=params, headers=headers)
        return r

    def get_content(self):
        pass

    def parce(self):
        pass