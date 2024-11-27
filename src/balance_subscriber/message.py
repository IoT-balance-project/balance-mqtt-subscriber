import datetime
from paho.mqtt.client import MQTTMessage


class Message:
    @classmethod
    def message_to_row(cls, message: MQTTMessage, encoding="utf-8") -> tuple:
        """
        Convert an incoming MQTT message to a row of data.
        """

        # Convert bytes to string
        # https://docs.python.org/3/library/stdtypes.html#bytes.decode
        payload = message.payload.decode(encoding=encoding)

        # Current timestamp ISO 8601
        # This is a bodge because MQTTMessage.timestamp is monotonic
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc)

        # timestamp = Monotonic time when the message was received
        # https://docs.python.org/3/library/time.html#time.monotonic
        return message.timestamp, current_timestamp.isoformat(), payload
