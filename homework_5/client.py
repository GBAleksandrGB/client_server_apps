"""Программа-клиент"""

import sys
import json
import socket
import time
import logging

import logs.config_client_log
import common.variables as var
from common.utils import get_message, send_message

logger = logging.getLogger('client')


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    """
    out = {
        var.ACTION: var.PRESENCE,
        var.TIME: time.time(),
        var.USER: {
            var.ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    """
    Функция разбирает ответ сервера
    """
    if var.RESPONSE in message:
        if message[var.RESPONSE] == 200:
            return '200 : OK'
        return logger.error(f'400 : {message[var.ERROR]}')
    raise ValueError


def main():
    """
    Загружаем параметы коммандной строки
    """
    logger.info('Cтарт клиента')

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])

        if not 1023 < server_port < 65536:
            logger.error(f'Недопустимый номер порта: {server_port}.')
            exit(1)
    except IndexError:
        server_address = var.DEFAULT_IP_ADDRESS
        server_port = var.DEFAULT_PORT
        logger.info(f'Установлены дефолтные значения адреса и порта.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    logger.info(
        f'Запущен клиент с парамертами:'
        f'  адрес сервера: {server_address},'
        f'  порт: {server_port}')
    message_to_server = create_presence()
    send_message(transport, message_to_server)

    try:
        answer = process_ans(get_message(transport))
        logger.info(f'Получен ответ: {answer}')
    except (ValueError, json.JSONDecodeError):
        logger.error('Не удалось декодировать сообщение сервера.')
        exit(1)


if __name__ == '__main__':
    try:
        main()
    except ConnectionRefusedError:
        logger.error('Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение.')
        exit(1)
