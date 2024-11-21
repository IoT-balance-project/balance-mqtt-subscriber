import argparse
import importlib.metadata
import logging
import paho.mqtt.client

import balance_subscriber.callbacks

logger = logging.getLogger(__name__)

DESCRIPTION = """
This is a simple script to test that the MQTT broker is working as expected. Use topics "#" to listen to all channels.
"""


def get_args():
    """
    Command-line arguments
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('topics', nargs='*', help="Topics to subscribe to, default: all", default='#')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=1883)
    parser.add_argument('--keepalive', type=int, default=60)
    parser.add_argument("--version", action="version",
                        version=importlib.metadata.version('balance-subscriber'))
    return parser.parse_args()


def get_client(topics) -> paho.mqtt.client.Client:
    # Initialise client
    client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)
    # https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html#logger
    client.enable_logger()
    # Make the topics available to the on_connect callback
    client.user_data_set(dict(topics=topics))

    # Register callbacks
    client.on_connect = balance_subscriber.callbacks.on_connect
    client.on_message = balance_subscriber.callbacks.on_message

    return client


def main():
    args = get_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # Connect to message broker
    client = get_client(topics=args.topics)
    client.connect(host=args.host, port=args.port, keepalive=args.keepalive)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
