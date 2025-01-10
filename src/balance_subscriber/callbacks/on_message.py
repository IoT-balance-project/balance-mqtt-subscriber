import logging
import uuid
from pathlib import Path
from paho.mqtt.client import MQTTMessage, Client

logger = logging.getLogger(__name__)


def on_message(client: Client, userdata: dict, msg: MQTTMessage):
    """
    The callback for when a PUBLISH message is received from the server.

    on_message callback
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_message

    MQTT message class
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.MQTTMessage
    """

    # File extension
    ext = userdata.get("ext", ".bin")

    # Convert an MQTT topic to a file path
    # E.g. 'plant/PL-f15320/Network' becomes 'plant/PL-f15320/Network'
    # Random unique filename
    path = Path(userdata["data_dir"]) / msg.topic / f"{uuid.uuid4().hex}{ext}"
    # Ensure subdirectory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Serialise payload
    # Error if the file already exists
    with path.open(mode="xb") as file:
        file.write(msg.payload)
