import logging

logger = logging.getLogger(__name__)


def on_connect_fail(client, userdata):
    """
    The callback called when the client failed to connect to the broker.
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_connect_fail

    Called by loop_forever() and loop_start() when the TCP connection failed to establish. This callback is not called
    when using connect() or reconnect() directly. It’s only called following an automatic (re)connection made by
    loop_start() and loop_forever()
    """
    logger.error("on_connect_fail")
    raise ConnectionRefusedError("on_connect_fail")
