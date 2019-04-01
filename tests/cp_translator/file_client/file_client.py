import logging.config

import os
import random

from cp_translator.file_client.exceptions import NoFileFoundException
from cp_translator import settings

logger = logging.getLogger(__name__)


def get_a_file_client(file_path):
    file_path = settings.test_harness_file_path
    file_client = FileClient(file_path)
    return file_client


class FileClient:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_a_random_file(self):
        try:
            list_files = os.listdir(self.file_path)
            if not list_files:
                raise NoFileFoundException()
            return random.choice(list_files)
        except NoFileFoundException as exc:
            logger.error('No file is present {}'.format(self.file_path))
            raise exc
        except Exception as exc:
            logger.error(exc, exc_info=True)
            raise exc
