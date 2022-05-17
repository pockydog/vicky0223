import requests
import chardet
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm

class DarazParser:
    def __init__(self):
        self.domain = 'https://www.daraz.pk'

    def get_product_url(self):
        url = 'https://www.daraz.pk/computing-storage/?page=0'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = soup.find_all('script')
        data = None
        for url in urls:
            if '<script>window.pageData=' in str(url):
                data = str(url)
        data = data.replace('window.pageData=', '').replace('<script>', '').replace('</script>', '')
        print(data)
        data = json.loads(data)
        data_list = data['mods']['listItems']
        http = ['https:' + data.get('productUrl') for data in data_list]
        return http

    def get_product_info(self):
        # urls = self.get_product_url()
        # for url in urls:
        url = 'https://www.daraz.pk/products/usb-32gb-20-i283578956-s1528219160.html?search=1'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        data = None
        for script in scripts:
            if 'app.run' in str(script):
                data = re.compile(r'{"data":((.*?))_popups"]}}}')
                data = data.search(str(script)).group(0)
                data = json.loads(data)
        product_ids = data['data']['root']['fields']['specifications']
        product_id = product_ids.keys()
        print(product_id)
        # product_id = re.sub(r'\D', '', str(product_id))
        # product_ids += data[product_id]['features']
        # print(product_ids)











            # title = data['name']
            # img_url = data['image']
            # price = data['price']

if __name__ == '__main__':
    DarazParser().get_product_url()
    DarazParser().get_product_info()
