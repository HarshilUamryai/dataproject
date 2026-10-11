import sys
import logging as Logger


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("Uncaught exception", exc_type, exc_value)

sys.excepthook = handle_exception

class CustomException(Exception):
    """Custom exception class for specific error handling."""
    pass
if __name__ == "__main__":
    Logger.info("Custom exception handling initialized.")
    try:
        raise CustomException("This is a custom exception.")
    except CustomException as e:
        print(f"Caught a custom exception: {e}")


            