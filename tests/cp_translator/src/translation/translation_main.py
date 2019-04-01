#!/usr/bin/python3
import logging.config
import signal
import sys
from pprint import pformat

from kafka.errors import NoBrokersAvailable, KafkaError
from shared.container import Container

from shared.exceptions import AvroException
from shared.initializers import (get_kafka_producer, get_service_bus_service, get_rema_avro_serializer,
                                 get_rema_avro_deserializer, get_kafka_consumer)

from translation import settings

# signal handler for Ctrl+C key press
from translation.processor.cp_processor import CPProcessor
from translation.processor.mapper import init_mapper
from translation.worker.translator_worker import TranslationWorker


def signal_handler(signal, frame):
    print('pressed Ctrl+C!')
    Container.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    try:
        logging.config.dictConfig(settings.logging)
        logger = logging.getLogger(__name__)
    except KeyError as exc:
        sys.exit('failed to create ' + exc.__str__())

    logger.info('currently applied settings........')
    for name, val in settings.__dict__.items():
        if name.startswith('__') or name.startswith('os') or name.startswith('str2bool'):
            continue
        logger.info('{} = {}'.format(name, pformat(val, indent=2)))

    try:
        kafka_consumer_settings = settings.inbound_client_settings
        kafka_producer_settings = settings.outbound_client_settings
        rema_message_schema = settings.rema_message_schema
        inbound_topic = settings.inbound_topic
        outbound_topic = settings.outbound_topic
        exception_topic = settings.exception_topic
    except (AttributeError, KeyError) as exc:
        sys.exit(exc)

        # we are overriding group_id
    kafka_consumer_settings['client_config']['group_id'] = '-'.join([inbound_topic, 'CP_TRANSLATOR_', 'CG'])

    workers_list = list()

    try:
        inbound_client = get_kafka_consumer(**kafka_consumer_settings)
    except (KeyError, AssertionError, NoBrokersAvailable, KafkaError, Exception) as exc:
            sys.exit('failed to create ' + exc.__str__())

    try:
        outbound_client = get_kafka_producer(**kafka_producer_settings)
    except (KeyError, AssertionError, NoBrokersAvailable, KafkaError, Exception) as exc:
        sys.exit('failed to create ' + exc.__str__())

    try:
        rema_avro_serializer = get_rema_avro_serializer(rema_message_schema)
    except (KeyError, AvroException) as exc:
        sys.exit('failed to create ' + exc.__str__())

    try:
        rema_avro_deserializer = get_rema_avro_deserializer(rema_message_schema)
    except (KeyError, AvroException) as exc:
        sys.exit('failed to create ' + exc.__str__())

    # translator_class = translator_mapping[translator]

    # mapping = None
    # if translator_mapping_file_path:
    #     with open(translator_mapping_file_path) as json_data:
    #         mapping = json.load(json_data)

    processor_kwargs = dict()
    processor_kwargs['avro_serializer'] = rema_avro_serializer
    processor_kwargs['avro_deserializer'] = rema_avro_deserializer

    mapper = init_mapper()

    kwargs = dict()
    kwargs['inbound_client'] = inbound_client
    kwargs['outbound_client'] = outbound_client
    kwargs['inbound_topic'] = inbound_topic
    kwargs['outbound_topic'] = outbound_topic
    kwargs['exception_topic'] = exception_topic
    kwargs['processor'] = CPProcessor(mapper)

    translation_worker = TranslationWorker(kwargs)
    workers_list.append(translation_worker)
    Container.start(translation_worker, 1)