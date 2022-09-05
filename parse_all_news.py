import re
import csv
import requests
from bs4 import BeautifulSoup

domain = 'https://pythondigest.ru'
url = f'{domain}/feed/'
# url = f'{domain}/feed/?q=Django'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

with open('parse_all.csv', mode='w', encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=',', lineterminator='\r')
    file_writer.writerow(['Число', 'Заголовок', 'Описание', 'Ссылка'])
    # Находим ссылкм для перехода на следующие страницы
    li = soup.find_all('li')
    # Запоминаем ко-во страниц, берем [-2], там будет число-последняя станица, [-1] это стрелка '->'
    page_count = li[-2].text
    # print(l.isdigit())
    # print(li[-2].text)
    # print(li[-2].a.get('href')[:-len(page_count)])
    # Запоминаем ссылку для перехода на следующую страницу /feed/?page=
    url_page = li[-2].a.get('href')[:-len(page_count)]
    # Проходим по страницам с 1 по кол-во страниц + 1
    for page in range(1, int(page_count) + 1):
        # Собираем url 'https://pythondigest.ru', '/feed/?page=', 'номер страницы'
        url3 = f'{domain}{url_page}{page}'
        # Отправляем запрос
        response = requests.get(url3)
        # Отправляем в библиотеку BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим место с новостями
        div = soup.find_all('div', class_='item-container')
        # Проходим по всем новостям на данной странице
        for news in div[:2]:
            # Находим место где стоит дата
            date = news.find('small').text
            # print(re.search('\d\d.\d\d.\d{4}', date)[0])
            # Берем только дату
            date = re.search(r'\d\d.\d\d.\d{4}', date)[0]
            # Вариант без использования регулярных выражений
            # print(date.split(' ')[1])
            # print(date)
            # Находим текст заголовка
            title = news.find('h4').text
            # print(title)
            # Находим ссылку
            link = news.find('h4').a.get('href')
            # Находим описание
            description = news.find_all('p')
            # Если оно есть
            if len(description) > 1:
                # print(description[1].text)
                # Записываем текст описания в переменную
                des = description[1].text
            # Иначе
            else:
                # Если описания нет, записываем в переменную 'Нет описания'
                des = 'Нет описания'
            # print('*****************************')
            # Записываем в csv строку с датой, заголовком и описанием
            file_writer.writerow([date, title, des, link])
