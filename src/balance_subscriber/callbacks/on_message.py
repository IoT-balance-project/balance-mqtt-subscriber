import datetime
import logging
import uuid
from pathlib import Path

import paho.mqtt

logger = logging.getLogger(__name__)


def on_message(
    client: paho.mqtt.client.Client, userdata, msg: paho.mqtt.client.MQTTMessage
):
    """
    The callback for when a PUBLISH message is received from the server.

    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_message
    """
    timestamp = datetime.datetime.fromtimestamp(msg.timestamp, datetime.timezone.utc)
    logger.debug(":%s:%s:%s", timestamp.isoformat(), msg.topic, msg.payload)

    # Serialise message
    filename = f"{uuid.uuid4().hex}.bin"
    path = Path() / filename
    with path.open("wb") as file:
        file.write(msg.payload)
        logger.debug("Wrote %s", file.name)
