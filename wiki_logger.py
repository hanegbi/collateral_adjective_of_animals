import logging
import sys
from logging import Logger

from consts import LOGGER_FILENAME, LOGGER_FORMAT


class WikiLogger:
    """
    Logger of logging.
    """

    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self) -> Logger:
        """
        Print the logger messages to stdout and write to logger.log.

        :return: Configured logger.
        """
        file_handler = logging.FileHandler(filename=LOGGER_FILENAME)
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(level=logging.DEBUG, format=LOGGER_FORMAT, handlers=[file_handler, stdout_handler])
        return logging.getLogger()

    def get_logger(self) -> Logger:
        """
        Get Logger.

        :return: Logger.
        """
        return self.logger
