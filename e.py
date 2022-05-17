import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

class GuardianProductHandler:
    def __init__(self):
        self.domain = 'https://www.guardian.com.sg'

    def get_page(self):
        url = f'{self.domain}/toiletries/bath-and-hand-cleansing/c/bath-and-hand-cleansing?q=%3Arelevance&page=1'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_item = soup.find('ul', {'class': 'pagination'})
        if not page_item:
            print('not get page item')
            return 0
        pages = page_item.text.strip()
        count = re.sub(r'\D', '', pages)
        return count

    def get_product_url(self):
        pages = self.get_page()
        url_list = list()
        for page in pages:
            url = f'{self.domain}/toiletries/bath-and-hand-cleansing/c/bath-and-hand-cleansing?q=%3Arelevance&page={page}'
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = soup.find_all('a', {'class': 'product-image pull-left thumb'})
            url_list += [url.get('href') for url in urls]
        return url_list

    def get_product_info(self):
        urls = self.get_product_url()
        product_list = list()
        name = None
        for url in tqdm(urls):
            url = f'{self.domain}{url}'
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('div', {'class': 'product-details'})
            for title in titles:
                name = title.find('h1', {'class': 'product_name_pdp'})
                if not name:
                    continue
                name = name.text
            price = soup.find('div', {'class': 'pull-right free'})
            description = soup.find('div', {'class': 'tab-details'}).text.replace('\n', '').lstrip()
            img_url = soup.find('a', {'class': 'active'}).get('data-image')
            type_items = soup.find_all('li', {'class': 'breadcrumb-item'})
            type_item = type_items[-1]

            if not (name and img_url and price and description and type_item):
                continue
            if '.' not in price.text:
                price_ = re.findall(r'\d+', price.text)[0]
            else:
                price_ = re.findall(r'\d.?\d+', price.text)[0].split('.')[0]
            type_ = type_item.text.replace('\r', '').replace('\t', '').strip()

            info = {
                'title': name,
                'price': price_,
                'img_url': img_url,
                'type': type_,
                'description': description
            }
            product_list.append(info)
        return product_list

    def exec(self):
        info_list = self.get_product_info()
        return info_list


if __name__ == '__main__':
    print(GuardianProductHandler().exec())
