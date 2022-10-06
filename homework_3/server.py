import socket
import json
import common.settings as var
from common.transport_params import TransportParams
from common.utils import MessageProcess


class Server(TransportParams):

    @staticmethod
    def process_client_message(message):

        if var.ACTION in message \
                and message[var.ACTION] == var.PRESENCE \
                and var.TIME in message \
                and var.USER in message \
                and message[var.USER][var.ACCOUNT_NAME] == 'Guest':
            return {var.RESPONSE: 200}
        return {
            var.RESPONSE: 400,
            var.ERROR: 'Bad Request'
        }

    @staticmethod
    def run():
        listen_port, listen_address = TransportParams.get_params(Server)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((listen_address, listen_port))
        transport.listen(var.MAX_CONNECTIONS)

        while True:
            client, client_address = transport.accept()
            print(client)

            try:
                message_from_client = MessageProcess.get_message(client)
                print(message_from_client)
                response = Server.process_client_message(message_from_client)
                MessageProcess.send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Принято некорректное сообщение от клиента.')
                client.close()


Server.run()
