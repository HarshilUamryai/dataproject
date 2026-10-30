import sys
from src.Logger import logging


def handle_exception(error, error_details=sys):
    exc_type, exc_value, tb = error_details.exc_info()
    if tb is None:
        logging.error(f"Error: {error}")
        return
    while tb.tb_next is not None:
        tb = tb.tb_next
    file_name = tb.tb_frame.f_code.co_filename
    line_number = tb.tb_lineno
    error_message = f"Error: {error} in file: {file_name} at line: {line_number}"
    logging.error(error_message, exc_info=(exc_type, exc_value, tb))


class CustomException(Exception):
    def __init__(self, error_message, error_details=None):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_traceback = (
            error_details.exc_info()[2]
            if error_details is not None
            else sys.exc_info()[2]
        )

    def __str__(self):
        tb = self.error_traceback or self.__traceback__
        if tb is None:
            return f"Error: {self.error_message}"
        while tb.tb_next is not None:
            tb = tb.tb_next
        file_name = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        return f"Error: {self.error_message} in file: {file_name} at line: {line_number}"


if __name__ == "__main__":
    try:
        x = 1 / 0
    except Exception as e:
        custom_exception = CustomException(str(e), sys)
        print(custom_exception)