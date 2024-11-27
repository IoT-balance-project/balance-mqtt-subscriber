import argparse
import importlib.metadata
import logging
import os
from pathlib import Path

import paho.mqtt.client

import balance_subscriber.callbacks

logger = logging.getLogger(__name__)

DESCRIPTION = """
This is an MQTT subscriber that serialises incoming messages.
"""


def get_args():
    """
    Command-line arguments
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--data_dir",
        type=Path,
        help="Directory to save messages to.",
        default=os.getenv("DATA_DIR"),
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument(
        "topics",
        nargs="*",
        help="Topics to subscribe to, default: all",
        default=os.getenv("TOPICS", "#"),
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "localhost"),
        help="MQTT broker host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 1883)),
        help="MQTT broker port",
    )
    parser.add_argument(
        "--keepalive",
        type=int,
        default=int(os.getenv("KEEP_ALIVE", 60)),
        help="MQTT broker keep-alive interval",
    )
    parser.add_argument("--encoding", default="utf-8", help="CSV output text character set")
    parser.add_argument(
        "--version",
        action="version",
        version=importlib.metadata.version("balance-subscriber"),
    )
    return parser.parse_args()


def get_client(topics: set[str], data_dir: Path) -> paho.mqtt.client.Client:
    if not data_dir:
        raise ValueError("No data directory specified")

    # Initialise client
    client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)
    # https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html#logger
    client.enable_logger()
    # Make the topics available to the on_connect callback
    client.user_data_set(dict(topics=topics, data_dir=data_dir, encoding=args.encoding))

    # Register callbacks
    client.on_connect = balance_subscriber.callbacks.on_connect
    client.on_message = balance_subscriber.callbacks.on_message

    return client


def main():
    args = get_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)

    # Connect to message broker
    client = get_client(topics=args.topics, data_dir=args.data_dir)
    client.connect(host=args.host, port=args.port, keepalive=args.keepalive)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
