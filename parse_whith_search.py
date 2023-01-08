import requests
from bs4 import BeautifulSoup
import re
import csv


def parser(search=None):
    domain = 'https://pythondigest.ru'

    if search:
        url = f'/feed/?q={search}'
    else:
        search = 'all'
        url = f'/feed/'

    # Создаем файл csv
    with open(f"search_{search}.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        # Записываем первую строку с названиями колонок
        file_writer.writerow(["Число", "Заголовок", "Описание", 'Ссылка'])
        # Если страниц в результате поиска новостей несколько
        # Пока есть ссылка на следующую страницу цикл выполняется
        while url:
            # Составляем url для получения страницы - domain + url
            # При первой итерации url будет тот который мы задали
            # При последующей url будет ссылка для перехода на следующую страницу если она есть
            url2 = f'{domain}{url}'
            # Отправляем запрос
            response = requests.get(url2)
            # Отправляем в библиотеку BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            li = soup.find_all('li')
            # Находим место с новостями
            div = soup.find_all('div', class_='item-container')
            # Проходим по всем новостям на данной странице
            for news in div:
                # Находим место, где стоит дата
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
                # print(news.find('h4').a.get('href'))
                # Находим описание
                description = news.find_all('p')
                # Если оно есть
                if len(description) > 1:
                    # print(description[1].text)
                    # Записываем текст описания в переменную
                    des = description[1].text
                # Иначе
                else:
                    # print('Нет описания')
                    # Если описания нет, записываем в переменную 'Нет описания'
                    des = 'Нет описания'
                # Записываем в csv строку с датой, заголовком, описанием и ссылкой
                file_writer.writerow([date, title, des, link])
                # print(li[-1].a.get('href'))
                # print(soup.find_all('ul', class_='pagination pagination-sm'))
            # Если страниц с новостями несколько(есть блок с номерами страниц)
            if soup.find_all('ul', class_='pagination pagination-sm'):
                # Записываем в url ссылку на следующую страницу
                url = li[-1].a.get('href')
            # Иначе(если блока с номерами страниц нет) выходим из цикла
            else:
                break
