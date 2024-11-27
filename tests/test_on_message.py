import csv
import datetime
import logging
import tempfile
import time
from pathlib import Path
import paho.mqtt.client
import balance_subscriber.callbacks

logger = logging.getLogger(__name__)


def test_on_message(caplog):
    # Message options
    client = None
    userdata = dict(data_dir=tempfile.mkdtemp())
    msg = paho.mqtt.client.MQTTMessage(mid=0, topic=b"plant/PL-f15320/Loadcell-B")
    msg.payload = b"471.22"
    msg.timestamp = time.monotonic()

    # Run callback
    balance_subscriber.callbacks.on_message(client, userdata, msg)

    path = Path(userdata["data_dir"]).joinpath("plant/PL-f15320/Loadcell-B.csv")
    assert path.exists()
    with path.open() as file:
        reader = csv.reader(file)
        row = next(reader)
        assert row[0] == str(msg.timestamp)
        datetime.datetime.fromisoformat(row[1])
        assert row[2] == msg.payload.decode("utf-8")
