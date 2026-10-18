import sys
from src.Logger import logging


def handle_exception(error, error_details: sys):
    _, _, tb = error_details.exc_info()
    file_name = tb.tb_frame.f_code.co_filename
    line_number = tb.tb_lineno
    error_message = f"Error: {error} in file: {file_name} at line: {line_number}"
    logging.error(error_message)


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_details = error_details

    def __str__(self):
        _, _, tb = self.error_details.exc_info()
        file_name = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        return f"Error: {self.error_message} in file: {file_name} at line: {line_number}"


if __name__ == "__main__":
    try:
        x = 1 / 0
    except Exception as e:
        custom_exception = CustomException(str(e), sys)
        print(custom_exception)