import Logger
import os
import datetime as dt

class Logger:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file

    def log(self, message):
        timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

    def clear_log(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

