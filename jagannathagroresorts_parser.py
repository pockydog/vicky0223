import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

class JagannathagroresortsParser:
    def __init__(self):
        self.domain = 'https://jagannathagroresorts.com'

    def get_page(self):
        url = f'{self.domain}/?post_type=product'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = soup.find('ul', {'class': 'page-numbers'})
        pages = pages.find_all('a')
        page_ = [re.sub(r'\D', '', page.text) for page in pages]
        return max(page_)

    def get_product_url(self):
        urls = self.get_page()
        url_list = list()
        for url in range(int(urls)+1):
            url = f'{self.domain}/?post_type=product&paged={url}'
            if '0' not in url:
                headers = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
                }
                response = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                product_urls = soup.find_all('a', {'class': 'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
                for product_url in product_urls:
                    url_list.append(product_url.get('href'))
        return url_list

    def get_product_info(self):
        urls = self.get_product_url()
        product_list = list()
        for url in tqdm(urls):
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
            }
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('h1', {'class': 'product_title entry-title'})
            price = soup.find('p', {'class': 'price'})
            price = price.find('ins')
            img_url = soup.find('div', {'class': 'woocommerce-product-gallery__image'})
            img_url = img_url.find('a')
            description = soup.find('div', {'class': 'woocommerce-product-details__short-description'})
            type_ = soup.find('nav', {'class': 'woocommerce-breadcrumb'})
            if not(name and price and img_url and description and type_):
                continue
            name = name.text
            type_ = type_.text.split('/')[1].replace('\xa0', '')
            description = description.text.strip().replace('\xa0', '')
            price = price.text
            price_ = re.findall(r'\d.?\d+', price)[0]
            img_url = img_url.get('href')
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
    JagannathagroresortsParser().exec()