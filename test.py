import re
import requests
from bs4 import BeautifulSoup


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
        for url in urls[:5]:
            url = f'{self.domain}{url}'
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            info = soup.find('div', {'class': 'itemDetailWrapper'})
            if not info:
                continue
            name_item = info.find('h1')
            price_item = info.find('div', {'class': 'priceWithDiscounts'})
            description_item = soup.find('div', {'class': 'moretext-content-wrapper'})
            type_item = soup.find('li', {'class': 'visited parent hasNext'})
            img_item = soup.find('a', {'class': 'linkToLImage cbox'})
            if not (name_item and price_item and description_item and type_item and img_item):
                continue

            name = name_item.text
            price = price_item.text
            price = re.findall(r'\d.?\d+', price)[0]
            description = description_item.text.strip().replace('\xa0', '&nbsp').replace('\n', '<\br>').replace('<\x08r>', '')
            type_ = type_item.text.strip()
            img_url = img_item.get('href')

            info = {
                'title': name,
                'price': price,
                'img_url': img_url,
                'type': type_,
                'description': description
            }
            product_list.append(info)
        return product_list

    def exec(self):
        info_list = self.get_product_info()
        print(info_list)
        return info_list


if __name__ == '__main__':
    product_list = KelabathParser().exec()

