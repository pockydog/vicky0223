import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
from tool import Tool


class Vicky:
    def __init__(self):
        self.domain = 'https://www.pinkoi.com'

    def get_links(self):
        count = 0
        page_list = list()
        while True:
            count += 1
            url = f'{self.domain}/browse?category=10&subcategory=1001&page={count}'
            soup = Tool.get_response(url=url)
            aoo = soup.select('script[type="application/ld+json"]')
            if len(aoo) < 2:
                break
            else:
                page_list.append(url)
        return page_list

    def get_url(self):
        urls = self.get_links()
        for url in urls:
            soup = Tool.get_response(url=url)
            aoo = soup.select('script[type="application/ld+json"]')
            results = json.dumps(str(aoo))
            results = results.split('\\"')
            final = [i for i in results if 'https://www.pinkoi.com/product/' in i]
            return final

    def get_info(self):
        result = list()
        urls = self.get_url()
        for url in tqdm(urls):
            soup = Tool.get_response(url=url)
            title = soup.find('title').text
            title = str(title).split('-')

            price = soup.find('div', {'class': 'price-wrap'}).text
            price = re.sub(r'\D', '', price)

            description = soup.find('div', {'class': 'm-richtext js-detail-content-inner'}).text
            description = description.replace('\n', '')

            img_url = soup.find('img', {'id': 'main-item-photo'}).get('src')
            info = {
                'title': title[0],
                'price': price,
                'img_url': f'https://{img_url}',
                'description': description
            }
            result.append(info)
        return result


if __name__ == '__main__':
    print(Vicky().get_info())
