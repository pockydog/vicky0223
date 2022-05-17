import requests
from bs4 import BeautifulSoup
# import re
import json;
import time


class Vicky:
    def __init__(self):
        self.domain = 'https://www.pinkoi.com'

    def get_link(self):
        count = 0
        time.sleep(0.01)
        page_list = list()
        while True:
            count += 1
            url = f'{self.domain}/browse?category=10&subcategory=1001&page={count}'
            print(url)
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 99.0.4844.84 Safari/537.36)'
            }
            response = requests.get(url=url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            aoo = soup.select('script[type="application/ld+json"]')
            if len(aoo) < 2:
                break
            else:
                page_list.append(url)
        return page_list



    # def get_links(self):
    #     url = f'{self.domain}/browse?category=10&subcategory=1001&page=50'
    #     headers = {
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 99.0.4844.84 Safari/537.36)'
    #     }
    #     response = requests.get(url=url, headers=headers)
    #     response.encoding = 'utf-8'
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     aoo = soup.select('script[type="application/ld+json"]')
    #     if len(aoo) < 2:
    #         print('shit')
    #
    #     # print(aoo)
    #
    # def get_link(self):
    #     time.sleep(0.001)
    #     url = f'{self.domain}/browse?category=10&subcategory=1001&page=2'
    #     headers = {
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 99.0.4844.84 Safari/537.36)'
    #     }
    #     response = requests.get(url=url, headers=headers)
    #     response.encoding = 'utf-8'
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     aoo = soup.select('script[type="application/ld+json"]')
    #     print(len(aoo))


if __name__ == '__main__':
    print(Vicky().get_link())
    print(Vicky().get_link())
