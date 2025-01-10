from pathlib import Path
from typing import Union

import paho.mqtt.client

import balance_subscriber.callbacks


def get_client(
    topics: set[str],
    data_dir: Union[str, Path],
    encoding: str = None,
    username: str = None,
    password: str = None,
    qos: int = 0,
    ext: str = None,
) -> paho.mqtt.client.Client:
    """
    Initialise the MQTT client
    """
    if not data_dir:
        raise ValueError("No data directory specified")

    encoding = encoding or "utf-8"
    ext = ext or ".bin"

    # Initialise client
    client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION2)
    # https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html#logger
    client.enable_logger()
    # Make the topics available to the on_connect callback
    client.user_data_set(
        dict(
            topics=topics, data_dir=Path(data_dir), encoding=encoding, qos=qos, ext=ext
        )
    )

    # Authentication
    if username:
        client.username_pw_set(username=username, password=password)

    # Register callbacks
    client.on_connect = balance_subscriber.callbacks.on_connect
    client.on_connect_fail = balance_subscriber.callbacks.on_connect_fail
    client.on_message = balance_subscriber.callbacks.on_message
    client.on_subscribe = balance_subscriber.callbacks.on_subscribe

    return client
