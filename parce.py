import requests
from bs4 import BeautifulSoup as bs
import csv


class Parce():
  
    csvfile = open('sample.csv', 'w', newline='', encoding='UTF-8')

    def __init__(self, url, params=None):

        self.url = url
        self.params = params
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.host = 'https://www.keramis.com.ua/'

    def html(self, url, params=None):
        """
        Получение html кода странички
        """
        r = requests.get(url, params=params, headers=self.headers)
        return r

    def get_pages_count(self, html):
        """
        Получение количества страничек
        """
        soup = bs(html, 'html.parser')
        try:

            pages_link = soup.find('span', class_='pagination_value_all').get_text()

            return int(pages_link)

        except:

            return 1

    def get_urls(self, html):
        """
        Получение ссылок на каждую карточку
        """

        soup = bs(html, 'html.parser')
        content = soup.find_all('div', class_='block_brief catalog__card')

        urls = []
        for cart in content:
            urls.append(self.host + cart.find('a').get('href'))

        return urls

    def get_content(self, html, url):
        """
        Получение информации с каждой странички товора
        """
        soup = bs(html, 'html.parser')

        # название+
        name = ''
        for name_1 in soup.find_all('h1', class_='product_title'):
            name = name_1.get_text().replace(';', ' ').replace(',', ' ')

        # цена+
        price = ''
        sale_price = ''

        for p in soup.find_all('div', class_='purchase'):
            price = p.find('div', class_='product_main_price').get_text()
            if p.find('span', class_='product_old_price') != None:
                sale_price = p.find('span', class_='product_old_price').get_text()
            

        # артикул+
        article = ''
        for article_1 in soup.find_all('span', class_='code_product'):
            article = article_1.get_text()

        # характеристики+
        properties = {}
        for i in soup.find_all('ul', class_='specifications_list'):
            for li in i.find_all('li'):
                span = li.find_all('span')
                a = li.find('a', class_='show-description')

                key = span[0].get_text().replace(';', ' ').replace(',', '.')
                value = span[-1].get_text().replace(';', ' ').replace(',', '.')

                properties[key] = value

        # хлебные крошки+
        breadcrumb = ''
        for breadcrumb_1 in soup.find_all('div', class_='breadcrumbs__list-wrapper'):
            breadcrumb = breadcrumb_1.get_text().replace(',', '.').replace('\n', '')

        # ссылки на картинки+
        image = ''
        for img in soup.find_all('div', class_='sl_banner_thumbs'):
            for i in img.find_all('img', class_='sl_banner_item'):
                if i.get('data-src') != None:
                    image += self.host + i.get('data-src') + '^'
                else:
                    image += self.host + i.get('src') + '^'

        content = {
            'url': url,
            'name': name,
            'price': price,
            'sale_price': sale_price,
            'article': article,
            'breadcrumb': breadcrumb,
            'properties': properties,
            'image': image,
        }

        return content

    def get_fieldnames(self, data):
        """
        Получаем характеристики в отдельный список
        """

        fieldnames = ['url', 'name', 'article', 'price', 'sale_price', 'breadcrumb', 'image']

        propertys = []
        for d in data:
            for key in d['properties']:
                propertys.append(key)

        fieldnames = fieldnames[0:6] + list(set(propertys)) + fieldnames[6:]

        return fieldnames

    def csv(self, data, csvfile=csvfile):

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=self.get_fieldnames(data))

        for d in data:
            for key, val in d['properties'].items():
                d.update({key: f"{key}: {val}"})

            d.pop('properties')    

        for d in data:
            writer.writerow(d)

    def parce(self):

        html = self.html(self.url)
        if html.status_code == 200:
            counter = self.get_pages_count(html.text)

            data = []
            for page in range(1, 2):

                print(f'\rWait, {page}/{counter}')

                html = self.html(self.url, params={'page': page})
                urls = self.get_urls(html.text)

                for url in urls:
                    html = self.html(url).text
                    data.append(self.get_content(html, url))

            self.csv(data)

        else:
            print('Something wrong!')

    
kranok = Parce('https://www.keramis.com.ua/category/plitka-dlja-vannoj-paradyz/')
kranok.parce()