import json
import socket
import time
import common.settings as var
from common.transport_params import TransportParams
from common.utils import MessageProcess


class Client(TransportParams):

    @staticmethod
    def create_presence(account_name='Guest'):

        out = {
            var.ACTION: var.PRESENCE,
            var.TIME: time.time(),
            var.USER: {
                var.ACCOUNT_NAME: account_name
            }
        }
        return out

    @staticmethod
    def process_ans(message):

        if var.RESPONSE in message:
            if message[var.RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[var.ERROR]}'
        raise ValueError

    @staticmethod
    def run():
        server_address, server_port = TransportParams.get_params(Client)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = Client.create_presence()
        MessageProcess.send_message(transport, message_to_server)

        try:
            answer = Client.process_ans(MessageProcess.get_message(transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось декодировать сообщение сервера.')


Client.run()
