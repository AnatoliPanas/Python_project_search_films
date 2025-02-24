import logging

class CustomLogger:
    def __init__(self, name: str, level=logging.INFO):
        logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._logger = logging.getLogger(name)

    def get_logger(self):
        return self._logger