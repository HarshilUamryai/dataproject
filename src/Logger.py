import logging as _logging
import os


class Logger:
    def __init__(self, log_file='logs/app.log'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)

        self.logger = _logging.getLogger('datascience_project')
        self.logger.setLevel(_logging.INFO)

        if not self.logger.handlers:
            handler = _logging.FileHandler(self.log_file)
            formatter = _logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def clear_log(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)


logging = Logger()

