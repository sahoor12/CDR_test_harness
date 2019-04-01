import os.path

inbound_topic = ""

outbound_topic = "REMA_COMPETITOR_PRICE_BLOB_VALID_TEST"

exception_topic = ""

test_harness_file_path = "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/data/"


inbound_client_settings= {
    "topics": [inbound_topic],
    "max_records": 1,
    "poll_timeout": 1000,
    "close_timeout": 5,
    "client_config": {
        "bootstrap_servers": "dev01-kafka-pollux-revionicsdev.aivencloud.com:23410",
        "security_protocol": "SSL",
        "ssl_cafile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/ca.pem",
        "ssl_certfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.cert",
        "ssl_keyfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.key",
        "enable_auto_commit": False,
        "auto_commit_interval_ms": 1000,
        "session_timeout_ms": 120000,
        "heartbeat_interval_ms": 40000,
        "auto_offset_reset": "earliest"
    }
}


outbound_client_settings= {
    "future_timeout": 5,
    "close_timeout": 5,
    "client_config": {
      "bootstrap_servers": "dev01-kafka-pollux-revionicsdev.aivencloud.com:23410",
      "security_protocol": "SSL",
        "ssl_cafile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/ca.pem",
        "ssl_certfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.cert",
        "ssl_keyfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.key",
      # "ssl_cafile": "/home/pavan/code/REMA/AZURE_SERVICEBUS/ssl/dev/ca.pem",
      # "ssl_certfile": "/home/pavan/code/REMA/AZURE_SERVICEBUS/ssl/dev/service.cert",
      # "ssl_keyfile": "/home/pavan/code/REMA/AZURE_SERVICEBUS/ssl/dev/service.key",
      "acks": 1,
      "retries": 1,
      "batch_size": 16384,
      "linger_ms": 5,
      "buffer_memory": 33554432,
      "connections_max_idle_ms": 540000,
      "max_block_ms": 60000,
      "max_request_size": 6048576,
      "metadata_max_age_ms": 300000,
      "retry_backoff_ms": 100,
      "request_timeout_ms": 30000,
      "max_in_flight_requests_per_connection": 5
    }
}

# outbound_client_settings= {
#     "future_timeout": 5,
#     "close_timeout": 5,
#     "client_config": {
#       "bootstrap_servers": "dev01-kafka-pollux-revionicsdev.aivencloud.com:23410",
#       "security_protocol": "SSL",
#       "ssl_cafile": "/home/himanshu/office/cp-translator/cp_translator/ssl/dev/ca.pem",
#       "ssl_certfile": "/home/himanshu/office/cp-translator/cp_translator/ssl/dev/service.cert",
#       "ssl_keyfile": "/home/himanshu/office/cp-translator/cp_translator/ssl/dev/service.key",
#       "acks": 1,
#       "retries": 1,
#       "batch_size": 16384,
#       "linger_ms": 5,
#       "buffer_memory": 33554432,
#       "connections_max_idle_ms": 540000,
#       "max_block_ms": 60000,
#       "max_request_size": 6048576,
#       "metadata_max_age_ms": 300000,
#       "retry_backoff_ms": 100,
#       "request_timeout_ms": 30000,
#       "max_in_flight_requests_per_connection": 5
#     }
# }
#
#
# outbound_client_settings= {
#     "future_timeout": 10,
#     "close_timeout": 5,
#     "aysnc": False,
#     "client_config": {
#         "bootstrap_servers": "dev01-kafka-pollux-revionicsdev.aivencloud.com:23410",
#         "security_protocol": "SSL",
#         "acks": 1,
#         "retries": 1,
#         "batch_size": 5242880,
#         "linger_ms": 5,
#         "buffer_memory": 33554432,
#         "connections_max_idle_ms": 540000,
#         "max_block_ms": 60000,
#         "max_request_size": 6048576,
#         "metadata_max_age_ms": 300000,
#         "retry_backoff_ms": 100,
#         "request_timeout_ms": 30000,
#         "max_in_flight_requests_per_connection": 5
#     }
# }

logging_kafka_client_settings = {
    "bootstrap_servers": "dev01-kafka-pollux-revionicsdev.aivencloud.com:23410",
    "security_protocol": "SSL",
    "ssl_cafile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/ca.pem",
    "ssl_certfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.cert",
    "ssl_keyfile": "/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/ssl/dev/service.key",
    "acks": 1,
    "retries": 1,
    "batch_size": 5242880,
    "linger_ms": 5,
    "buffer_memory": 33554432,
    "connections_max_idle_ms": 540000,
    "max_block_ms": 60000,
    "max_request_size": 6048576,
    "metadata_max_age_ms": 300000,
    "retry_backoff_ms": 100,
    "request_timeout_ms": 30000,
    "max_in_flight_requests_per_connection": 5
}

# timeout in seconds
http_settings = {
    "timeout": 5,
    "max_retries": 1
}

rema_message_schema ={
    "type": "record",
    "name": "RemaMessage",
    "namespace": "com.rema.revionics.dde.avro",
    "doc": "This is a Rema Message Avro schema.",
    "fields": [
        {
            "name": "Body",
            "type": "string"
        },
        {
            "name": "BrokerProperties",
            "type": {
                "type": "map",
                "values": "string"
            }
        },
        {
            "name": "topic",
            "type": "string",
            "default": "null"
        },
        {
            "name": "blob_xml",
            "type": "string",
            "default": "null"
        },
        {
            "name":"blob_name",
            "type":"string",
            "default": "null"
        }
    ]
}


logging = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler"
        },
        'file': {
            'backupCount': 10,
            'level': 'INFO',
            'maxBytes': 1048576,
            'encoding': 'utf-8',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "_".join([inbound_topic.lower(), "cp_translater-consumer.log"])
        }
    },

    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True
        },
        "kafka": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True
        },
        "requests": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

options = {
    "log_level": "DEBUG",
    "mapping": {
        "file_path": "./",
        "file_name": "mapping.json"
    }
}


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


# docker container path for logs
docker_log_path = '/app/logs'
