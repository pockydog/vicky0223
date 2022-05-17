import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import json

class ExsysProductHandler:
    def __init__(self):
        self.domain = 'https://www.exsys-shop.de'

    def get_product_page(self):
        url = f'{self.domain}/shopware/en/widgets/listing/listingCount/sCategory/13?p=1&c=13&o=1&n=12&loadProducts=1'
        response = requests.get(url=url)
        responses = json.loads(response.text)['pagination']
        soup = BeautifulSoup(responses, 'html.parser')
        pages = soup.find_all('a', {'class': 'paging--link paging--next'})
        for page in pages:
            if 'Last page' in str(page):
                ans = page.get('href')
                counts = re.search(r'p=(\d+)', ans).group(1)
                url_list = [f'{self.domain}/shopware/en/categories/usb-products/?p={count}' for count in range(int(counts)+1)]
                return url_list

    def get_product_url(self):
        urls = self.get_product_page()
        product_list = list()
        for url in urls:
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_url = soup.find_all('div', {'class': 'product--info'})
            for product in product_url:
                product = product.find('a', {'class': 'product--image'}).get('href')
                product_list.append(product)
        return product_list

    def get_product_info(self):
        urls = self.get_product_url()
        result = list()
        final_type = None
        for url in tqdm(urls):
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('div', {'class': 'product--info'}).text
            description = soup.find('div', {'class': 'product--description'}).text
            img_url = soup.find('span', {'class': 'image--media'})
            img_url = img_url.find('img').get('src')
            price = soup.find('span', {'class': 'price--content content--default'}).text
            price = re.findall(r'\d.?\d+', price)[0]
            types = soup.find_all('span', {'class': 'breadcrumb--title'})
            for type_ in types:
                if 'Overview' in type_.text and 'Categories' in type_.text:
                    continue
                final_type = type_.text

            info = {
                'title': name.strip(),
                'price': price,
                'img_url': img_url,
                'type': final_type,
                'description': description.strip()
            }
            result.append(info)
        return result

    def exec(self):
        info_list = self.get_product_info()
        return info_list


if __name__ == '__main__':
    print(ExsysProductHandler().exec())
