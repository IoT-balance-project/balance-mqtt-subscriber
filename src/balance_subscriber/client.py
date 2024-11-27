from pathlib import Path
from typing import Union

import paho.mqtt

import balance_subscriber.callbacks


def get_client(
    topics: set[str], data_dir: Union[str, Path], encoding: str = "utf-8"
) -> paho.mqtt.client.Client:
    """
    Initialise the MQTT client
    """
    if not data_dir:
        raise ValueError("No data directory specified")

    # Initialise client
    client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)
    # https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html#logger
    client.enable_logger()
    # Make the topics available to the on_connect callback
    client.user_data_set(
        dict(topics=topics, data_dir=Path(data_dir), encoding=encoding)
    )

    # Register callbacks
    client.on_connect = balance_subscriber.callbacks.on_connect
    client.on_message = balance_subscriber.callbacks.on_message

    return client
