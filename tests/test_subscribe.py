import tempfile
import uuid

from balance_subscriber.client import get_client

HOSTNAME = "test.mosquitto.org"


def test_publish():
    topic = uuid.uuid4().hex
    with tempfile.NamedTemporaryFile() as temp:
        client = get_client(topics={topic}, data_dir=temp.name)
        client.connect(host=HOSTNAME)
        client.subscribe(topic)
        client.unsubscribe(topic)
        client.disconnect()
