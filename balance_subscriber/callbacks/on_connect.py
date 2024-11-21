import logging

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, reason_code, properties):
    """
    The callback for when the client receives a CONNACK response from the server.
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_connect
    """
    logger.info(f"Connected with result code {reason_code}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in userdata['topics']:
        client.subscribe(topic)
        logger.info("Subscribed to %s", topic)
