import balance_subscriber.message
import paho.mqtt.client


def test_message_to_row():
    message = paho.mqtt.client.MQTTMessage(mid=42, topic=b"plant/PL-f15320/Temperature")
    row = balance_subscriber.message.Message.message_to_row(message)
    assert isinstance(row, tuple)
