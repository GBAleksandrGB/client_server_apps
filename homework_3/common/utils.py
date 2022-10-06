import json
from .settings import MAX_PACKAGE_LENGTH, ENCODING


class MessageProcess:

    @staticmethod
    def get_message(client):
        """
        Утилита приёма и декодирования сообщения.
        Принимает байты, выдаёт словарь, если принято что-то
        другое возвращает ValueError (ошибку значения)
        """
        encoded_response = client.recv(MAX_PACKAGE_LENGTH)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode(ENCODING)
            if isinstance(json_response, str):
                response = json.loads(json_response)
                if isinstance(response, dict):
                    return response
                raise ValueError
            raise ValueError
        raise ValueError

    @staticmethod
    def send_message(sock, message):
        """
        Утилита кодирования и отправки сообщения:
        принимает для отправки словарь, получает из него строку,
        далее превращает строку в байты и отправляет.
        """
        if not isinstance(message, dict):
            raise TypeError
        js_message = json.dumps(message)
        encoded_message = js_message.encode(ENCODING)
        sock.send(encoded_message)
