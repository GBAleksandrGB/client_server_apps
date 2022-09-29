import platform
import subprocess

from chardet import detect

print('task_1'.center(50, '*'))


# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.


def check_type(*args):
    [print(type(arg), end='|') for arg in args]
    print()


if __name__ == '__main__':
    check_type('разработка', 'сокет', 'декоратор')
    check_type('\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
               '\u0441\u043e\u043a\u0435\u0442',
               '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')

print('task_2'.center(50, '*'))


# 2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
# а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя методы
# encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.


def convert_string_to_bytes(*args):
    for arg in args:
        result = eval(f'b"{arg}"')
        print(result, type(result), len(result))


if __name__ == '__main__':
    convert_string_to_bytes('class', 'function', 'method')

print('task_3'.center(50, '*'))


# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
# Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.


def check_convert_string_to_bytes(*args):
    for arg in args:

        try:
            print(bytes(arg, encoding='ASCII'))
        except UnicodeEncodeError:
            print(f'"ascii" codec can`t encode characters in word "{arg}": ordinal not in range(128)\n'
                  f'try "UTF-8"')
            print(bytes(arg, encoding='UTF-8'))

        continue


if __name__ == '__main__':
    check_convert_string_to_bytes('attribute', 'класс', 'функция', 'type')

print('task_4'.center(50, '*'))


# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).


def convert_string(*args):
    enc_result = (arg.encode('UTF-8') for arg in args)

    for el in enc_result:
        print(el)
        print(el.decode('UTF-8'))


if __name__ == '__main__':
    convert_string('разработка', 'администрирование', 'protocol', 'standard')

print('task_5'.center(50, '*'))


# 5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат
# из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.


def ping_sites(site: str):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    base = ['ping', param, '1', site]
    subproc_ping = subprocess.Popen(args=base, stdout=subprocess.PIPE)

    for line in subproc_ping.stdout:
        result = detect(line)
        line = line.decode(result['encoding']).encode('UTF-8')
        print(line.decode('UTF-8'))


if __name__ == '__main__':
    ping_sites('yandex.ru')
    ping_sites('youtube.com')

print('task_6'.center(50, '*'))


# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Далее забыть о том, что мы сами только что создали этот файл
# и исходить из того, что перед нами файл в неизвестной кодировке.
# Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.


def create_file(*args):
    with open('test_file.txt', 'w', encoding='UTF-8') as f:
        f.writelines([arg + '\n' for arg in args])


def open_file(filename):
    with open(filename, 'rb') as f:
        enc = detect(f.read())['encoding']

    with open(filename, encoding=enc) as f:
        print(f.read())


if __name__ == '__main__':
    create_file('сетевое программирование', 'сокет', 'декоратор')
    open_file('test_file.txt')
