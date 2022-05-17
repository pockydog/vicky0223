import requests
from bs4 import BeautifulSoup
import re
import time


class Vicky:

    def __init__(self):
        self.domain = 'https://icook.tw'

    def get_page(self):
        count = 0
        cake_url = list()
        while True:
            count +=1
            time.sleep(0.1)
            url = f'{self.domain}/search/%E7%B0%A1%E5%96%AE%E9%AC%86%E9%A4%85/?page={count}'
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36) '
                }
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            page = soup.find_all('a', {'class': 'browse-recipe-link'})
            if not page:
                break
            else:
                cake_url.append(url)
        return cake_url

    def get_links(self):
        product = list()
        urls = self.get_page()
        for url in urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36) '
            }
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            page_ = soup.find_all('a', {'class': 'browse-recipe-link'})
            for page in page_:
                content_url = page.find('article', {'class': 'browse-recipe-card'}).get('id')
                re_content_url = re.sub(r'\D', '', content_url)
                product.append(f'{self.domain}/recipes/{re_content_url}')
        return product

    def get_product_info(self):
        urls = self.get_links()
        result = list()
        for url in urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36) '
            }
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            img = soup.find('a', {'class': 'glightbox ratio-container ratio-container-4-3'}).get('href')
            name = soup.find('h1', {'class': 'title'}).text

            contents = soup.find('div', {'class': 'group group-0'})
            data_name = contents.find_all('a')
            content_name = [i.text for i in data_name]
            ingredient_unit = contents.find_all('div', {'class': 'ingredient-unit'})
            content_num = [i.text for i in ingredient_unit]
            zip_content = dict(zip(content_name, content_num))
            context = ''
            for key, value in zip_content.items():
                context += f'{key}: {value}</br>'

            # list 改 str 方法
            # aa = [f'{content_name[i]}:{content_num[i]}' for i in range(len(content_name))]
            # aaa = '</br>'.join(aa)

            articles = soup.find('ul', {'class': 'recipe-details-steps'}).text
            description = articles.replace('\n', '')

            info = {
                'title': name,
                'content': context,
                'img_url': img,
                'description': description
            }
            result.append(info)

        return result


    def exec(self):
        info_list = self.get_product_info()
        return info_list


if __name__ == '__main__':
    print(Vicky().exec())
