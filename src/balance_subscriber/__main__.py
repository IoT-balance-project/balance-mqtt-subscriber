import argparse
import importlib.metadata
import logging
import os
from pathlib import Path

from balance_subscriber.client import get_client

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
        "-d",
        type=Path,
        help="Directory to save messages to.",
        default=os.getenv("DATA_DIR"),
    )
    parser.add_argument(
        "--log_level",
        default=os.getenv("LOG_LEVEL", "WARNING"),
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
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
    parser.add_argument(
        "--encoding", default="utf-8", help="CSV output text character set"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=importlib.metadata.version("balance-subscriber"),
    )
    parser.add_argument("--username", "-u", default=os.getenv("USERNAME"))
    parser.add_argument("--password", "-p", default=os.getenv("PASSWORD"))
    parser.add_argument(
        "-q", "--qos", type=int, choices={0, 1, 2}, default=0, help="Quality of service"
    )
    parser.add_argument(
        "-e",
        "--ext",
        default=os.getenv("EXT", ".bin"),
        help="File extension for saved data.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(level=args.log_level)

    # Connect to message broker
    client = get_client(
        topics=args.topics,
        data_dir=args.data_dir,
        encoding=args.encoding,
        username=args.username,
        password=args.password,
        qos=args.qos,
        ext=args.ext,
    )
    client.connect(host=args.host, port=args.port, keepalive=args.keepalive)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
