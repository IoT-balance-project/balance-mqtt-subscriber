from pathlib import Path


class Topic:
    def __init__(self, topic: str):
        self.topic = str(topic)

    def __str__(self):
        return self.topic

    def to_path(self, data_dir: Path) -> Path:
        """
        Convert an MQTT topic to a file path
        E.g. 'plant/PL-f15320/Network' becomes 'plant/PL-f15320/Network.csv'
        """
        # Create a directory based on topic name
        path = Path(data_dir) / f"{self.topic}.csv"
        # Ensure subdirectory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
