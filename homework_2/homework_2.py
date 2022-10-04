from glob import glob
import re
import csv
import locale
import json
import yaml
from yaml.loader import SafeLoader
from pprint import pprint

from chardet.universaldetector import UniversalDetector
from chardet import detect

print('task_1'.center(50, '*'))


# a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие
# и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения
# параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
# в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data
# — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла);
# b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
# данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# c. Проверить работу программы через вызов функции write_to_csv().


def get_data(path):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [
        ['Изготовитель системы', '«Название ОС', 'Код продукта', 'Тип системы']
    ]

    def get_value(elem):
        return re.match(r'(.*):\s{1,}(.*)$', elem.strip()).group(2)

    detector = UniversalDetector()

    for file in glob(path):
        detector.reset()

        for line in open(file, 'rb'):
            detector.feed(line)

            if detector.done:
                break

        detector.close()
        enc = detector.result['encoding']

        with open(file, encoding=enc) as f:

            for line in f:

                if 'Изготовитель системы' in line:
                    os_prod_list.append(get_value(line))

                if 'Название ОС' in line:
                    os_name_list.append(get_value(line))

                if 'Код продукта' in line:
                    os_code_list.append(get_value(line))

                if 'Тип системы' in line:
                    os_type_list.append(get_value(line))

    for prod, name, code, type in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append([prod, name, code, type])

    return main_data


def write_to_csv(file):
    data = get_data(path='info_files/*')

    with open(file, 'w', encoding='UTF-8', newline='') as f:
        f_writer = csv.writer(f)
        f_writer.writerows(data)

    with open(file, encoding='UTF-8') as test:
        test_reader = csv.reader(test)
        pprint(list(test_reader), width=100)


if __name__ == '__main__':
    write_to_csv(file='main_data.csv')

print('task_2'.center(50, '*'))


# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря
# в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.


def write_order_to_json(**kwargs):
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump({'orders': [kwargs]}, f, indent=4, ensure_ascii=False)

    pprint(json.load(open('orders.json', encoding='utf-8')))


if __name__ == '__main__':
    item = 'Корм для кошек 1+'
    quantity = 5
    price = 25.00
    buyer = 'Александр'
    date = '2022-10-02'
    write_order_to_json(item=item, quantity=quantity, price=price, buyer=buyer, date=date)

print('task_2'.center(50, '*'))


# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных
# в файле YAML-формата. Для этого:
# a. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму —
# целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
# отсутствующим в кодировке ASCII (например, €);
# b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
# При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность
# работы с юникодом: allow_unicode = True;
# c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.


data_to_yaml = {'list': ['LITE', None, True], 'int': 42, 'dict': {'price1': '13€', 'price2': '5€'}}


def write_to_yaml(data):
    with open('file.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    with open('file.yaml', encoding='utf-8') as f:
        content = yaml.load(f, Loader=SafeLoader)
        print(content)
        print(content == data_to_yaml)


if __name__ == '__main__':
    write_to_yaml(data_to_yaml)
