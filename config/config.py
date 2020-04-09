import sys
import logging
import configparser


logger = logging.getLogger(__name__)

cfg = configparser.ConfigParser()


try:
    cfg.read('config.ini')
except FileNotFoundError as error:
    logger.error(error)
    sys.exit(1)