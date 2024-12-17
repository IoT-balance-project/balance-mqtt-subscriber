import logging

from paho.mqtt.reasoncodes import ReasonCode

logger = logging.getLogger(__name__)


def on_connect(client, userdata, connect_flags, reason_code: ReasonCode, properties):
    """
    The callback for when the client receives a CONNACK response from the server.
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_connect
    """
    logger.info("Reason code: '%s'", reason_code)

    if reason_code.is_failure:
        raise ConnectionError(reason_code)

    # Quality of service
    qos = userdata.get("qos", 0)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in userdata["topics"]:
        logger.info("Attempting to subscribe to topic '%s'...", topic)
        client.subscribe(topic, qos=qos)
