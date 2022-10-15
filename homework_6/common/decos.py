"""Декораторы"""

import sys
import logging
import inspect
from functools import wraps

sys.path.append('../')
import logs.config_server_log
import logs.config_client_log


def deco(func):
    """Функция-декоратор"""

    @wraps(func)
    def log_saver(*args, **kwargs):
        logger = logging.getLogger('server' if 'server.py' in sys.argv[0] else 'client')
        result = func(*args, **kwargs)
        logger.info(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}.'
                    f'Вызов из модуля {func.__module__}.'
                    f'Вызов из функции {inspect.stack()[1][3]}')
        return result
    return log_saver

