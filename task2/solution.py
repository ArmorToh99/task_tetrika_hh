"""
Необходимо реализовать скрипт, который будет получать с русскоязычной википедии список всех животных
(https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту) и записывать в файл в формате beasts.csv количество
животных на каждую букву алфавита. Содержимое результирующего файла:
    А,642
    Б,412
    В,....
Примечание:
анализ текста производить не нужно, считается любая запись из категории (в ней может быть не только название, но и,
например, род)

Можно использовать библиотеки. К задаче должны быть написаны тесты.
"""
import unittest
import requests
import pandas
from bs4 import BeautifulSoup


def get_animals_value(html):
    bs4 = BeautifulSoup(html, 'html.parser')
    item_list = bs4.find('div', attrs={'class': 'mw-category-columns'}).text.split("\n")
    item_list = [item for item in item_list if len(item) > 1]
    for item in item_list:
        if item[0] not in animals_dict.keys():
            animals_dict[item[0]] = 0
        else:
            animals_dict[item[0]] += 1
    return bs4


animals_dict = {}

html = requests.get('https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту').text
bs4_returned = get_animals_value(html)

while True:
    page = bs4_returned.find('a', string='Следующая страница')
    if page is None:
        break
    next_page = str(page).split('"')[1].split('amp;')
    url = 'https://ru.wikipedia.org' + next_page[0] + next_page[1]
    html = requests.get(url).text
    bs4_returned = get_animals_value(html)


key_list = []
value_list = []

for key, value in animals_dict.items():
    key_list.append(key)
    value_list.append(value)

res = {'letter': key_list, 'value': value_list}

df = pandas.DataFrame(res)
df.to_csv('output.csv', index=False, encoding='cp1251', header=False)