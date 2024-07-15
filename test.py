import logging
import configparser

class Logger:
    def __init__(self, config_file='./config/logging.ini'):
        self.config = self._parse_config(config_file)

        self.logger = logging.getLogger('FileManagerLogger')
        self._setup_logger()

        self.special_logger = logging.getLogger('SpecialOperationsLogger')
        self._setup_special_logger()

    def _parse_config(self, config_file):
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file)
        return config

    def get_config(self, section, key):
        if self.config.has_section(section):
            return self.config.get(section, key)
        else:
            raise KeyError(f"Section {section} not found in the configuration file")

    def _setup_logger(self):
        log_level = self.get_config('common', 'level')
        log_format = self.get_config('common', 'format')
        date_format = self.get_config('common', 'datefmt')
        filename = self.get_config('common', 'filename')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(logging.Formatter(log_format, date_format))

        self.logger.setLevel(getattr(logging, log_level))
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def _setup_special_logger(self):
        level = self.get_config('special', 'level')
        filename = self.get_config('special', 'filename')
        format = self.get_config('special', 'format')
        datefmt = self.get_config('special', 'datefmt')

        special_file_handler = logging.FileHandler(filename)
        special_file_handler.setLevel(getattr(logging, level))
        special_file_handler.setFormatter(logging.Formatter(format, datefmt))

        self.special_logger.setLevel(getattr(logging, level))
        self.special_logger.addHandler(special_file_handler)

    def get_logger(self):
        return self.logger

    def get_special_logger(self):
        return self.special_logger

# Example usage
if __name__ == "__main__":
    logger = Logger()
    file_logger = logger.get_logger()
    special_logger = logger.get_special_logger()

    file_logger.info("This is a log message")
    special_logger.info("This is a log message")
    file_logger.debug("Debug message")
    special_logger.debug("Debug message")
