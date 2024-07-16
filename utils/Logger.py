import configparser
import logging
import sys


class Logger:

    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('../config/logging.ini')


    def get_common_logger(self):
        logger = logging.getLogger('CLogger')
        level = self.get_config('common', 'level')
        format = self.get_config('common', 'format')
        datefmt = self.get_config('common', 'datefmt')
        filename = self.get_config('common', 'filename')
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
        level = self.get_config('special', 'level')
        format = self.get_config('special', 'format')
        datefmt = self.get_config('special', 'datefmt')
        filename = self.get_config('special', 'filename')
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter(format))
        steam_handler = logging.StreamHandler(sys.stdout)
        steam_handler.setLevel(logging.INFO)
        logger.setLevel(level)
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(steam_handler)
        return logger

    def get_config(self, section, key):
        if self.config.has_section(section):
            return self.config.get(section, key)
        else:
            raise KeyError(f"Section {section} not found in the configuration file")



# if __name__ == '__main__':
#     logger = Logger()
#     CLogger = logger.get_common_logger()
#     SLogger = logger.get_special_logger()
#     CLogger.info('xixi')
#     CLogger.debug('xixi')
#     SLogger.info('xixi')
#     SLogger.debug('xixi')



