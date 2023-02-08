import requests
from bs4 import BeautifulSoup

URL = 'https://alser.kz'

def get_soup(URL):
    r = requests.get(URL, verify=False)
    soup = BeautifulSoup(r.text)
    return soup

parenet_categories = [
    (i['href'], i.text) 
    for i 
    in get_soup(URL).find_all('a', class_='categories-item')
    ]

res_list = []

for category_link, category_name in parenet_categories:
    sub_categories = get_soup(URL + category_link).find_all('div', class_='categories__item')
    for sub_category in sub_categories:
        sub_category_name = sub_category.find('div', class_='categories__item_title').text
        sub_category_link = sub_category.find('a', class_='categories__item_image')['href']
        sub_sub_categories = get_soup(URL + sub_category_link).find_all('div', class_='categories__item')
        for sub_sub_category in sub_sub_categories:
            sub_sub_category_name = sub_sub_category.find('div', class_='categories__item_title').text
            sub_sub_category_link = sub_sub_category.find('a', class_='categories__item_image')['href']
            i = 1
            while True:
                r = requests.get(URL + sub_sub_category_link + f'/page-{i}', verify=False)
                soup = BeautifulSoup(r.text)
                prod_details = [i for i in soup.find_all('div', class_='product-item')]
                if prod_details:
                    for prod_detail in prod_details:
                        name_tab = prod_detail.find('a', class_='product-item__info_title')
                        name = name_tab.text
                        link = URL + name_tab['href']
                        price = prod_detail.find('div', class_='price').text

                        res = {
                            'name': name, 
                            'price': price, 
                            'link': link,
                            'category': sub_sub_category_name,
                            'sub_category': sub_category_name,
                            'parent_category': category_name
                            }

                        res_list.append(res)
                    i += 1
                else:
                    break