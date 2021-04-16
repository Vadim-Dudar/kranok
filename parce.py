import requests
from bs4 import BeautifulSoup as bs
import sys
import csv
import time
from threading import Thread


class Parce():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    def __init__(self, url, params=None):

        self.url = url
        self.params = params
        # self.csvfile = open('sample.csv', 'w', newline='')
        # self.writer = csv.writer(self.csvfile)

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

    def get_content(self, html, url):

        soup = bs(html, 'html.parser')
        content = []

        for name in soup.find_all('div', class_='product-title'):
            content.append(name.find('h1').get_text())

        for p in soup.find_all('div', class_='pr-q'):
            if p.find('span', class_='price') != None:
                content.append(p.find('span', class_='price').get_text().replace('\n', '').replace('\xa0', ' '))
            else:
                bprice = p.find('div', class_='b-price').get_text().replace('\n', '').replace('\xa0', ' ')
                aprice = p.find('div', class_='price-old').get_text().replace('\n', '').replace('\xa0', ' ')
                content.append(f'{bprice}, {aprice}')


        for i in soup.find_all('ul')[2:4]:
            for li in i.find_all('li'):
                span = li.find_all('span')
                content.append(f'{span[0].get_text()}: {span[1].get_text()}')

        imgstr = ''
        for img in soup.find_all('div', class_='viewport'):
            for i in img.find_all('a'):
                imgstr += i.get('href') + ', ' 
            print(imgstr)

        content.append(imgstr)

        content.insert(0, url)
        return content

    def csv(self, data):

        with open('sample.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(i for i in data)
            writer.writerow('\n')
            print('new card')

    def parce(self):

        html = self.html(self.url)
        if html.status_code == 200:
            counter = self.get_pages_count(html.text)

            for page in range(1, counter+1):
                html = self.html(self.url, params={'page': page})
                urls = self.get_urls(html.text)
                    
                for url in urls:
                    print(url)
                    html = self.html(url).text
                    self.csv(self.get_content(html, url))

        else:
            print('Something wrong!')

    
kranok = Parce('https://kranok.ua/ua/smesiteli-dlja-vannoj')
kranok.parce()