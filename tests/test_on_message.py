import logging
import tempfile
import time

import paho.mqtt.client
import balance_subscriber.callbacks

logger = logging.getLogger(__name__)


def test_on_message():
    # Message options
    userdata = dict(data_dir=tempfile.mkdtemp())
    msg = paho.mqtt.client.MQTTMessage(mid=0, topic=b"plant/PL-f15320/Loadcell-B")
    msg.payload = b'{"value": "471.22"}'
    msg.timestamp = time.monotonic()

    # Run callback
    balance_subscriber.callbacks.on_message(None, userdata, msg)
