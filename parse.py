import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from decorators import benchmark

count = 0


def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='hotel-by-stars')
    products = product_list.find_all('li', class_='grid')

    for product in products:
        try:
            photo = product.find('div', class_='load gallery-popup-wrapper hotel-popup-trigger').find('img').get('src').split('//')[-1]
        except:
            photo = ''

        try:
            title = product.find('div', class_='hotel-info').text
        except:
            title = ''

        try:
            score = product.find('p', class_='rating').text
        except:
            score = ''

        data = {'title': title, 'score': score, 'photo': photo}
        write_csv(data)
    return True


def write_csv(data):
    with open('hotel.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['score'], data['photo']))
        print(f'{data["title"]} - парсятся!')


def prepare_csv():
    global count
    with open('hotel.csv', 'w') as file:
        fieldnames = ['Название', "Фото", "Рейтинг"]
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow({
            'Название': 'Название',
            'Фото': 'Фото',
            'Рейтинг': 'Рейтинг'
        })


def make_all(link):
    data = get_html(link)
    res = get_data(data)
    write_csv(res)


@benchmark
def main():
    prepare_csv()
    start = datetime.now()
    for i in range(0, 10):
        main_url = f'https://www.hotels.ru/rus/hotels/russia/cities.htm'
        html = get_html(main_url)
        is_res = get_data(html)

        if not is_res:
            break

    finish = datetime.now()
    print(f'Парсинг занял: {finish - start}')


if __name__ == '__main__':
    main()


