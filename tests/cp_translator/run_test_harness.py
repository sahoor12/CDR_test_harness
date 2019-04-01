import signal
import sys
import logging.config

from cp_translator.test_harness.test_harness import TestHarness, get_a_test_harness
from cp_translator import settings

def signal_handler(signal, frame):
    if TestHarness.event.is_set():
        TestHarness.event.clear()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    test_harness = get_a_test_harness()
    test_harness.run()
