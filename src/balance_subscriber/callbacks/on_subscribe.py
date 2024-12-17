import logging

from paho.mqtt.reasoncodes import ReasonCode

from balance_subscriber.exceptions import SubscriptionError

logger = logging.getLogger(__name__)


def on_subscribe(client, userdata, mid, reason_code_list: list[ReasonCode], properties):
    """
    This callback is called when the broker responds to a subscribe request, sending a SUBACK response.
    https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.on_subscribe
    """

    for reason_code in reason_code_list:
        if reason_code.is_failure:
            raise SubscriptionError(reason_code)
        logger.info("Subscribed. Reason code '%s'", reason_code)
