import json
from abc import ABC, abstractmethod
from kafka import KafkaProducer

class IOutputStrategy(ABC):
    @abstractmethod
    def output_data(self, data: list):
        pass

class ConsoleOutputStrategy(IOutputStrategy):
    def output_data(self, data: list):
        for item in data:
            identifier = item.get("SystemAccount", "Unknown")
            print(f"DEBUG [Console]: Processing Employee {identifier}")

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, broker: str, topic: str):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=[self.broker],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def output_data(self, data: list):
        for item in data:
            identifier = item.get("SystemAccount", "Unknown")
            print(f"SEND [Kafka]: Topic '{self.topic}' <- Row {identifier}")
            self.producer.send(self.topic, item)
        self.producer.flush()