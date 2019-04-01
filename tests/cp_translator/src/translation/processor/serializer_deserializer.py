import logging

from shared.exceptions import InvalidMessageException

logger = logging.getLogger(__name__)


class TranslationSerde:

    def __init__(self, avro_serializer, avro_deserializer):
        """
        :param avro_serializer: rema specific avro_serializer
        :type avro_serializer: AvroSerializer
        :param avro_deserializer: rema specific avro_deserializer
        :type avro_deserializer: AvroDeserializer
        """
        self.avro_serializer = avro_serializer
        self.avro_deserializer = avro_deserializer

    def serialize_message(self, message):
        """
        serialize the message

        :param message: serialize the rema message
        :type message: dict
        :return: returns serialized message
        :rtype: bytearray
        """

        try:
            serialized_message = self.avro_serializer.writer(message)
            return serialized_message
        except Exception as exc:
            logger.error(exc, exc_info=True)
            msg = 'unable to serialize the message'
            raise InvalidMessageException(msg) from exc

    def deserialize_message(self, message):
        """
        deserialize avro message
        :param message: avro serialized rema message
        :type message: bytearray
        :return: rema message
        :rtype: dict
        """

        try:
            deserialized_message_records = self.avro_deserializer.reader(message)
            deserialized_message = next(deserialized_message_records)
            logger.debug('deserialized message is {}'.format(deserialized_message))
            return deserialized_message
        except Exception as exc:
            msg = 'unable to deserialize message - {}'.format(message)
            logger.error(msg)
            raise InvalidMessageException(msg) from exc
