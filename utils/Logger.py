import configparser
import logging
import sys


class Logger:

    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('../config/logging.ini')


    def get_common_logger(self):
        logger = logging.getLogger('CLogger')
        level = self.config.get('common', 'level')
        format = self.config.get('common', 'format')
        datefmt = self.config.get('common', 'datefmt')
        filename = self.config.get('common', 'filename')
        handlers = self.config.get('common', 'handlers')
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter(format))
        steam_handler = logging.StreamHandler(sys.stdout)
        steam_handler.setLevel(logging.INFO)
        logger.setLevel(level)
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(steam_handler)
        return logger


    def get_special_logger(self):
        logger = logging.getLogger('SLogger')
        level = self.config.get('special', 'level')
        format = self.config.get('special', 'format')
        datefmt = self.config.get('special', 'datefmt')
        filename = self.config.get('special', 'filename')
        handlers = self.config.get('special', 'handlers')
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter(format))
        steam_handler = logging.StreamHandler(sys.stdout)
        steam_handler.setLevel(logging.INFO)
        logger.setLevel(level)
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(steam_handler)
        return logger





if __name__ == '__main__':
    logger = Logger()
    CLogger = logger.get_common_logger()
    SLogger = logger.get_special_logger()
    CLogger.info('xixi')
    CLogger.debug('xixi')
    SLogger.info('xixi')
    SLogger.debug('xixi')



