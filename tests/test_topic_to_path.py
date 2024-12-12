import tempfile
from pathlib import Path
import balance_subscriber.topic


def test_topic_to_path():
    topic = balance_subscriber.topic.Topic("plant/PL-f15320/Loadcell-B")
    data_dir = tempfile.mkdtemp()
    path = topic.to_path(data_dir=data_dir)
    assert isinstance(path, Path)
    assert path == Path(data_dir) / "plant/PL-f15320/Loadcell-B.csv"
