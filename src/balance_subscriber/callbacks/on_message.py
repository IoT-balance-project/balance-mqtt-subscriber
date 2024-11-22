import csv
import datetime
import logging
from pathlib import Path

import paho.mqtt.client

logger = logging.getLogger(__name__)


def on_message(
        client: paho.mqtt.client.Client, userdata: dict, msg: paho.mqtt.client.MQTTMessage
):
    """
    The callback for when a PUBLISH message is received from the server.

    on_message callback
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_message

    MQTT message class
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.MQTTMessage
    """
    # Build file path
    # Create a directory based on topic name
    # Remove the path root (we want to make a subdirectory in our data directory)
    # E.g. '/plant/PL-f15320/Network' becomes 'plant/PL-f15320/Network.csv'
    topic_path = Path(msg.topic.lstrip('/') + '.csv')
    path = Path(userdata["data_dir"]) / topic_path

    # Ensure directory exits
    path.parent.mkdir(parents=True, exist_ok=True)

    # Convert bytes to string
    # https://docs.python.org/3/library/stdtypes.html#bytes.decode
    payload = msg.payload.decode(encoding='utf-8')

    # Append to CSV file
    with path.open("a") as file:
        writer = csv.writer(file)
        writer.writerow((msg.timestamp, payload))
