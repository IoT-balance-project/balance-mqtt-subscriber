import csv
import datetime
import logging
from pathlib import Path

from paho.mqtt.client import Client, MQTTMessage

logger = logging.getLogger(__name__)


def on_message(client: Client, userdata: dict, msg: MQTTMessage):
    """
    The callback for when a PUBLISH message is received from the server.

    on_message callback
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_message

    MQTT message class
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.MQTTMessage
    """

    ext = userdata.get("ext") or ".csv"
    "File extension"
    encoding = userdata.get("encoding") or "utf-8"
    data_dir = Path(userdata["data_dir"])
    "The root directory for serialising messages."

    # Convert an MQTT topic to a file path
    # E.g. 'plant/PL-f15320/Network' becomes 'plant/PL-f15320/Network.csv'
    path = data_dir / f"{msg.topic}{ext}"
    # Ensure subdirectory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Build data row
    row = (
        # Current timestamp
        datetime.datetime.now(datetime.UTC).isoformat(),
        msg.payload.decode(encoding),
    )

    # Serialise payload by appending a row to the CSV file
    with path.open(mode="a", encoding=encoding) as file:
        writer = csv.writer(file)
        writer.writerow(row)
