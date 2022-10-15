"""Программа-сервер"""

import socket
import sys
import json
import logging

import common.variables as var
from common.utils import get_message, send_message
from common.decos import deco
import logs.config_server_log

logger = logging.getLogger('server')


@deco
def process_client_message(message):
    """Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, возвращает словарь - ответ для клиента
    """

    if var.ACTION in message and message[var.ACTION] == var.PRESENCE and \
            var.TIME in message and \
            var.USER in message and \
            message[var.USER][var.ACCOUNT_NAME] == 'Guest':
        return {var.RESPONSE: 200}
    return {
        var.RESPONSE: 400,
        var.ERROR: 'Bad Request'
    }


def main():
    """Загрузка параметров командной строки, если нет параметров,
    то задаём значения по умолчанию. Сначала обрабатываем порт
    """

    logger.info('Cтарт сервера')

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = var.DEFAULT_PORT
        if not 1023 < listen_port < 65536:
            logger.error(f'Недопустимый номер порта: {listen_port}.')
            exit(1)
    except IndexError:
        logger.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        logger.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''

    except IndexError:
        logger.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    logger.info(f'Запущен сервер с параментрами: адрес - {listen_address}, порт - {listen_port}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(var.MAX_CONNECTIONS)
    logger.info('Сервер слушает')

    while True:
        client, client_address = transport.accept()

        try:
            message_from_client = get_message(client)
            logger.info(f'Получено сообщение от клиента: {message_from_client}')
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
            logger.info('Клиент успешно отправил сообщение.')
        except (ValueError, json.JSONDecodeError):
            client.close()
            logger.error('Принято некорректное сообщение от клиента.')


if __name__ == '__main__':
    main()
