
from kafka import KafkaProducer
import json
from kafka_config import KAFKA_TOPIC, KAFKA_SERVER

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(message):
    producer.send(KAFKA_TOPIC, message)
    producer.flush()
