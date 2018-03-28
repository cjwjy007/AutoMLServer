import traceback

from automl.logger.logger import Logger


class ErrHandler:
    @staticmethod
    def handle_err(e):
        Logger.write_log(e)
        print(e)
        traceback.print_exc()
        return False
