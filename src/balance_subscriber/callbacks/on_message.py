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
    timestamp = datetime.datetime.fromtimestamp(msg.timestamp, datetime.timezone.utc)
    logger.debug(":%s:%s:%s", timestamp.isoformat(), msg.topic, msg.payload)

    # Build file path
    # Create a directory based on topic name
    topic_path = Path(msg.topic)
    # Remove the path root (we want to make a subdirectory in our data directory)
    # E.g. '/plant/PL-f15320/Network' becomes 'plant/PL-f15320/Network'
    topic_path = topic_path.relative_to(topic_path.root)
    # E.g. '/mnt/data/plant/PL-f15320/Network/193.bin'
    filename = f"{msg.mid}.bin"  # message identifier
    path = Path(userdata["data_dir"]) / topic_path / filename

    # Serialise binary data
    with path.open("wb") as file:
        file.write(msg.payload)
        logger.info("Wrote %s", file.name)
