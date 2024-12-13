import csv
import logging
from paho.mqtt.client import MQTTMessage, Client
from balance_subscriber.message import Message
from balance_subscriber.topic import Topic

logger = logging.getLogger(__name__)


def on_message(_: Client, userdata: dict, msg: MQTTMessage):
    """
    The callback for when a PUBLISH message is received from the server.

    on_message callback
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_message

    MQTT message class
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.MQTTMessage
    """
    logger.debug("Recived. Topic: %s Message: %s", msg.topic, msg.payload)

    row = Message.message_to_row(msg, encoding=userdata.get("encoding", "utf-8"))
    path = Topic(msg.topic).to_path(data_dir=userdata["data_dir"])
    # Append to CSV file
    with path.open(mode="a") as file:
        writer = csv.writer(file)
        writer.writerow(row)
