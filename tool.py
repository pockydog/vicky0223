import requests
from bs4 import BeautifulSoup

class Tool:
    @classmethod
    def get_response(cls, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 99.0.4844.84 Safari/537.36)'
        }
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup



