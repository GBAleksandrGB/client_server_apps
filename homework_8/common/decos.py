"""Декораторы"""

import sys
import logging

# from ..logs import config_server_log
# from ..logs import config_client_log


def log(func_to_log):
    """Функция-декоратор"""

    def log_saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)

        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret

    return log_saver
