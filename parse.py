from bs4 import BeautifulSoup
import requests
import datetime
import csv
from decorators import benchmark
from multiprocessing import Pool

count = 0


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


# def get_hotels_links(html):
#     urls = []
#     soup = BeautifulSoup(html, 'lxml')
#     catalog = soup.find('div', class_='a8b500abde').find('div', class_='eef2c3ca89').find('ol', class_='a8b500abde')
#     items = catalog.find_all('li', class_='f32a99c8d1')
#     for item in items:
#         a = item.find('a').get('href')
#         link = 'https://www.mashina.kg' + a
#         urls.append(link)
#     return urls


# def get_all_links():
#     links = []
#     for i in range(0, 16):
#         url = f'https://www.booking.com/searchresults.html?sid=fd4bbab3236f8084d78c9e0d9acc6a97&aid=337554&dest_id=-2331392&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&offset=75{i*25}'
#         html = get_html(url)
#         hotels_links = get_hotels_links(html)
#         links.extend(hotels_links)
#     return links

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_url = soup.find('div', class_='a8b500abde').find('ol', class_='a8b500abde')
    last_page = pages_url.find_all('li', class_='f32a99c8d1')[-1]
    total_pages = last_page.find('button').get('area_label').split('=')[-1]
    return int(total_pages)


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')

    product_list = soup.find('div', 'dcf496a7b9').find('div', 'd4924c9e74')
    products = product_list.find_all('div', class_='d20f4628d0')

    for product in products:
        try:
            photo = product.find('div', class_='c90a25d457').find('a').find('img').get('data-src')
        except:
            photo = ''

        try:
            title = product.find('div', class_='b978843432').find('div', class_='fcab3ed991 a23c043802').text
        except:
            title = ''

        try:
            description = product.find('div', class_='b978843432').find('div', class_='d8eab2cf7f').text
        except:
            description = ''

        data = {'title': title, 'description': description, 'photo': photo}
        print(data)

    # catalog = soup.find('div', class_='d4924c9e74')
    # if not catalog:
    #     False
    #
    # title = catalog.find('div', class_='fcab3ed991 a23c043802').text.strip()
    # description = catalog.find('div', class_='d8eab2cf7f')
    # # names = (x.text for x in description.find_all('span', class_='name'))
    # # values = (y.text for y in description.find_all('span', class_='value'))
    # # desc = {x: y for x, y in zip(names, values)}
    #
    # rating = catalog.find('div', class_='a1b3f50dcd cbb2d85c33 a1f3ecff04 db7f07f643 d19ba76520 d02f1578ba d17b3fe5e2').find('div', 'b5cd09854e d10a6220b4').text.strip()
    # try:
    #     image = catalog.find('div', class_="c90a25d457").find('img').get('data-src')
    # except:
    #     image = 'Нет картинки!'
    # data = {
    #     'title': title,
    #     'rating': rating,
    #     'img': image,
    #     'description': description
    # }
    # return data

#
# def write_csv(data):
#     with open('hotel.csv', 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow((data['title'], data['rating'], data['img'], data['description']))
#         print(f'{data["title"]} - парсятся!')
#
#
# def prepare_csv():
#     global count
#     with open('hotel.csv', 'w') as file:
#         fieldnames = ['Название', "Рейтинг", "Фото", "Описание"]
#         writer = csv.DictWriter(file, fieldnames)
#         writer.writerow({
#             'Название': 'Название',
#             'Рейтинг': 'Рейтинг ',
#             'Фото': 'Фото',
#             'Описание': 'Описание'
#         })
#
#
# def make_all(link):
#     data = get_html(link)
#     res = get_data(data)
#     write_csv(res)


# @benchmark
def main():
    url = 'https://www.booking.com/searchresults.html?sid=fd4bbab3236f8084d78c9e0d9acc6a97&aid=337554&dest_id=-2331392&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&offset=0'
    get_total_pages(url)
    get_data(get_html(url))

    # prepare_csv()
    # links = get_all_links()
    # start = datetime.now()
    # with Pool(40) as pool:
    #     pool.map(make_all, links)
    # finish = datetime.now()
    # print(f'Парсинг занял: {finish - start}')


if __name__=='__main__':
    main()


