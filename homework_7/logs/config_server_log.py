import sys
import logging.handlers
import os

sys.path.append('../')
from common.variables import LOGGING_LEVEL, ENCODING

formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

stream = logging.StreamHandler(sys.stderr)
stream.setFormatter(formatter)

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')
file = logging.handlers.TimedRotatingFileHandler(
    path, encoding=ENCODING, interval=3, when='D', backupCount=10, utc=True)
file.setFormatter(formatter)

logger = logging.getLogger('server')
logger.addHandler(stream)
logger.addHandler(file)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.critical('Critical')
    logger.error('Error')
    logger.warning('Warning')
    logger.info('Info')
    logger.debug('Debug')
