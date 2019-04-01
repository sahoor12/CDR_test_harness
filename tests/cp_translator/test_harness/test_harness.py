import json
import logging.config
import random
import sys

import time
from kafka.errors import NoBrokersAvailable, KafkaError, CommitFailedError

from shared.exceptions import AvroException, InvalidMessageException
from shared.initializers import get_settings, get_kafka_producer, get_rema_avro_serializer

from cp_translator.file_client.file_client import get_a_file_client
from cp_translator import settings
from cp_translator.src.translation.processor.cp_processor import CPProcessor
from cp_translator.src.translation.processor.mapper import init_mapper
from cp_translator.src.translation.worker.translator_worker import TranslationWorker

MESSAGES_COUNT = 20

logger = logging.getLogger(__name__)


def get_a_test_harness():

    try:
        logger = logging.getLogger(__name__)
    except KeyError as exc:
        sys.exit('failed to create ' + exc.__str__())

    try:
        kafka_producer_settings = settings.outbound_client_settings
        outbound_client = get_kafka_producer(**kafka_producer_settings)
    except (KeyError, AssertionError, NoBrokersAvailable, KafkaError, Exception) as exc:
        sys.exit('failed to create ' + exc.__str__())
    try:
        rema_message_schema = settings.rema_message_schema
        rema_avro_serializer = get_rema_avro_serializer(rema_message_schema)
    except (KeyError, AvroException) as exc:
        sys.exit('failed to create ' + exc.__str__())

    outbound_topic = settings.outbound_topic
    exception_topic = settings.exception_topic

    mapper = init_mapper()
    processor = CPProcessor(mapper)

    kwargs = dict()
    kwargs['inbound_client'] = None
    kwargs['outbound_client'] = outbound_client
    kwargs['outbound_topic'] = outbound_topic
    kwargs['exception_topic'] = exception_topic
    kwargs['processor'] = processor
    file_path = settings.test_harness_file_path
    file_client = get_a_file_client(file_path)
    test_harness = TestHarness(kwargs, file_client, outbound_topic)
    return test_harness


class Message:
    def __init__(self, value):
        self.value = value


class TestHarness(TranslationWorker):
    def __init__(self, kwargs, file_client, outbound_topic):
        self.file_client = file_client
        self.outbound_topic = outbound_topic
        super(TestHarness, self).__init__(kwargs)

    def get_message(self):
        file = self.file_client.get_a_random_file()
        file_path = settings.test_harness_file_path + file
        with open(file_path) as f:
            data = json.load(f)
        return data

    def run(self):
        #for the limited number of fake_price file data to be sent to write the code here. Count the number of files in the directory then run the while loop till that
        while True:
            message = self.get_message()
            self.process_and_dispatch_message(message)

    def process_and_dispatch_message(self, message):
        """
        process and dispatch the message

        :param message: kafka consumer record
        :type message: list
        :raises InvalidMessageException: if message is invalid
        :raises HttpError: if unable to download the blob
        :raises KafkaError: if unable to send to outbound client
        :raises CommitFailedError: if unable to commit the message
        """
        try:
            print("Sending messaege into kafka - ", message)
            results = self.processor.map(message)
            results = json.dumps(results)
            results = results.encode()
            logger.debug('Translated results: {}.'.format(results))
            self.send(self.outbound_topic, results)
            logger.debug("Successfully sent message into kafka - ", results)
        except (KeyError, InvalidMessageException, KafkaError, CommitFailedError, Exception) \
                as exc:
            logger.error(exc)
