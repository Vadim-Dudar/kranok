import requests
from bs4 import BeautifulSoup as bs
import sys


class Parce():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    def __init__(self, url, params=None):

        self.url = url
        self.params = params

    def html(self, url, params=None, headers=headers):

        r = requests.get(url, params=params, headers=headers)
        return r

    def get_pages_count(self, html):
        soup = bs(html, 'html.parser')
        pages_link = soup.find('a', class_='last').get('href')
        
        page = ''
        for i in pages_link[::-1]:
            try:
                page += str(int(i))
            except:
                break

        return int(page[::-1])

    def get_urls(self, html):

        soup = bs(html, 'html.parser')
        content = soup.find_all('div', class_='product-main')

        urls = []
        for cart in content:
            urls.append(cart.find('a').get('href'))

        return urls

    def get_content(self, html):

        soup = bs(html, 'html.parser')
        feature = soup.find_all('ul')

        spans = []
        for i in feature[2:4]:
            for li in i.find_all('li'):
                d = []
                for span in li.find_all('span'):
                    d.append(span.get_text())
                    # spans.append(span.get_text())
                spans.append(d)

        print(spans)
        return spans

    def csv(self, data):
        pass

    def parce(self):

        html = self.html(self.url)
        if html.status_code == 200:
            counter = self.get_pages_count(html.text)
            for page in range(1, counter+1):
                html = self.html(self.url, params={'page': page})
                urls = self.get_urls(html.text)
                for url in urls:
                    print(url)
                    html = self.html(url)
                    self.get_content(html.text)
                    # sys.stdout.write(f'\rWait, {page}/{counter}')       
        else:
            print('Something wrong!')

    
kranok = Parce('https://kranok.ua/ua/smesiteli-dlja-vannoj')
kranok.parce()