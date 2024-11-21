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

    # Serialise message
    filename = f"{msg.mid}.bin"  # message identifier
    # Create a directory based on topic name
    path = Path(userdata["data_dir"]) / msg.topic / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as file:
        file.write(msg.payload)
        logger.debug("Wrote %s", file.name)
