import tempfile
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.packettypes import PacketTypes
import balance_subscriber.callbacks
import balance_subscriber.client


def test_on_connect():
    topics = {"topic1/subtopic1", "topic1/subtopic2", "topic2/subtopic1"}
    client = balance_subscriber.client.get_client(
        topics=topics, data_dir=tempfile.mkdtemp(), encoding="utf-8"
    )
    userdata = dict(topics=topics)
    reason_code = ReasonCode(PacketTypes.DISCONNECT)
    balance_subscriber.callbacks.on_connect(client, userdata, None, reason_code, None)
