import json
import logging
import ast

from kafka.errors import KafkaError, CommitFailedError
from kafka.producer.future import FutureRecordMetadata

from shared.exceptions import InvalidMessageException
from shared.worker import BaseWorker

logger = logging.getLogger(__name__)


class TranslationWorker(BaseWorker):

    def __init__(self, kwargs):
        """
        :Keyword Arguments

        - inbound_client (`Any`) - kafka inbound client for consuming the messages
        - outbound_client (`Any`) - kafka outbound client for sending the processed information
        - inbound_topic (`str`) - kafka topic to consume
        - outbound_topic (`str`) - kafka topic to send
        - exception_topic (`str`) - kafka exception topic for sending invalid messages
        - processor (`Any`) - message processor to process the message
        """

        inbound_client = kwargs.get('inbound_client')
        outbound_client = kwargs.get('outbound_client')
        inbound_topic = kwargs.get('inbound_topic')
        outbound_topic = kwargs.get('outbound_topic')
        exception_topic = kwargs.get('exception_topic')

        super(__class__, self).__init__(inbound_client, outbound_client,
                                        inbound_topic, outbound_topic, exception_topic)

        self.processor = kwargs.get('processor')

    @staticmethod
    def on_send_success(record_metadata):
        logger.info('Topic-{}, partition-{}, offset-{}'.format(record_metadata.topic, record_metadata.partition, record_metadata.offset))

    @staticmethod
    def on_send_error(excp, messageId=None, blob_name=None):
        logger.event(excp, extra={'blob_name': blob_name, 'messageId': messageId})

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
            results = self.processor.map(message)
            print("results are - ", results)
            logger.debug('Translated results: {}.'.format(results))
            super().commit(message)
        except (KeyError, InvalidMessageException, KafkaError, CommitFailedError, Exception)  as exc:
            logger.error(exc)
