import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

class KelabathParser:
    def __init__(self):
        self.domain = 'https://www.kela.de'

    def get_page(self):
        url = f'{self.domain}/en/bath/bath-accessories/'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = soup.find_all('a', {'class': 'pageLink'})
        page_ = [page.get('href') for page in pages]
        return page_

    def get_product_url(self):
        urls = self.get_page()
        url_list = list()
        for url in urls:
            url = f'{self.domain}{url}'
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', {'class': 'itemWrapper'})
            url_list += [product.find('a').get('href') for product in products]
        return url_list

    def get_product_info(self):
        urls = self.get_product_url()
        product_list = list()
        for url in tqdm(urls):
            url = f'{self.domain}{url}'
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            info = soup.find('div', {'class': 'itemDetailWrapper'})
            if not info:
                continue
            name = info.find('h1').text
            price = info.find('div', {'class': 'priceWithDiscounts'}).text
            price_ = re.findall(r'\d.?\d+', price)[0]
            description = soup.find('div', {'class': 'moretext-content-wrapper'}).text.strip().replace('\xa0', '&nbsp')
            type_ = soup.find('li', {'class': 'visited parent hasNext'}).text.strip()
            img_url = soup.find('a', {'class': 'linkToLImage cbox'}).get('href')
            info = {
                'title': name,
                'price': price_,
                'img_url': img_url,
                'type': type_,
                'description': description
            }
            product_list.append(info)
        print(product_list)
        return product_list

    def exec(self):
        info_list = self.get_product_info()
        return info_list


if __name__ == '__main__':
    KelabathParser().exec()