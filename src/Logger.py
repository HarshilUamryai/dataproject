import logging as _logging
import os
from pathlib import Path


class Logger:
    def __init__(self, log_file='logs/app.log'):
        log_path = Path(log_file)
        if not log_path.is_absolute():
            log_path = Path(__file__).resolve().parents[1] / log_path
        self.log_file = str(log_path)
        os.makedirs(os.path.dirname(self.log_file) or '.', exist_ok=True)

        self.logger = _logging.getLogger('datascience_project')
        self.logger.setLevel(_logging.INFO)

        if not self.logger.handlers:
            handler = _logging.FileHandler(self.log_file)
            formatter = _logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message, exc_info=None):
        self.logger.error(message, exc_info=exc_info)

    def exception(self, message, exc_info=True):
        self.logger.exception(message, exc_info=exc_info)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def clear_log(self):
        if not os.path.exists(self.log_file):
            return

        log_path = str(Path(self.log_file).resolve())
        for handler in self.logger.handlers:
            if (
                isinstance(handler, _logging.FileHandler)
                and handler.baseFilename == log_path
            ):
                handler.acquire()
                try:
                    handler.flush()
                    if handler.stream is not None:
                        handler.stream.seek(0)
                        handler.stream.truncate()
                finally:
                    handler.release()
                return

        with open(self.log_file, "w", encoding="utf-8"):
            pass


logging = Logger()
