import logging

from filepath import log_dir


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def write_log(msg, log_type=None):
        try:
            LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
            DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

            logging.basicConfig(filename='%s/log.txt' % log_dir, level=logging.DEBUG, format=LOG_FORMAT,
                                datefmt=DATE_FORMAT)
            if not log_type:
                logging.info(msg)
            elif log_type == 'error':
                logging.error(msg)
        except FileNotFoundError as e:
            print(e)
