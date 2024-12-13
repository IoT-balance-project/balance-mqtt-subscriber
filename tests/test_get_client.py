import tempfile

import balance_subscriber.client


def test_get_client():
    balance_subscriber.client.get_client(
        topics={"topic1/subtopic1", "topic1/subtopic2", "topic2/subtopic1"},
        data_dir=tempfile.mkdtemp(),
        encoding="utf-8",
    )
