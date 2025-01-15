import csv
import datetime
import logging
import tempfile
import time
import struct
from pathlib import Path

import paho.mqtt.client
import pytest
import balance_subscriber.callbacks

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("payload", ["471.22", 471.22, "disabled", 123, "192.168.1.199"])
def test_on_message(payload):
    # Message options
    encoding = "utf-8"
    userdata = dict(data_dir=tempfile.mkdtemp(), encoding=encoding)
    topic = "plant/PL-f15320/Loadcell-B"

    # Build MQTT message
    msg = paho.mqtt.client.MQTTMessage(mid=0, topic=topic.encode(encoding))
    msg.payload = str(payload).encode(encoding)
    msg.timestamp = time.monotonic()

    # Run callback
    balance_subscriber.callbacks.on_message(None, userdata, msg)

    # Check data has been serialised to CSV
    path = Path(userdata["data_dir"]).joinpath(f"{topic}.csv")
    with path.open() as file:
        reader = csv.reader(file)
        row = next(reader)
        timestamp, value = row

        # Check data types
        datetime.datetime.fromisoformat(timestamp)
        assert isinstance(value, str)
        assert value == str(payload)
