import sys
from .settings import DEFAULT_PORT, DEFAULT_IP_ADDRESS


class TransportParams:

    @staticmethod
    def get_params(cls):

        if cls.__name__ == 'Server':
            try:
                if '-p' in sys.argv:
                    listen_port = int(sys.argv[sys.argv.index('-p') + 1])
                else:
                    listen_port = DEFAULT_PORT

                if listen_port < 1024 or listen_port > 65535:
                    raise ValueError

            except IndexError:
                print('После параметра -\'p\' необходимо указать номер порта.')
                sys.exit(1)
            except ValueError:
                print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
                sys.exit(1)

            try:
                if '-a' in sys.argv:
                    listen_address = sys.argv[sys.argv.index('-a') + 1]
                else:
                    listen_address = ''

            except IndexError:
                print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
                sys.exit(1)

            return listen_port, listen_address

        if cls.__name__ == 'Client':

            try:
                server_address = sys.argv[1]
                server_port = int(sys.argv[2])
                if server_port < 1024 or server_port > 65535:
                    raise ValueError
            except IndexError:
                server_address = DEFAULT_IP_ADDRESS
                server_port = DEFAULT_PORT
            except ValueError:
                print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
                sys.exit(1)

            return server_address, server_port
