from kafka import KafkaConsumer
import json
from kafka_config import KAFKA_TOPIC, KAFKA_SERVER

def get_latest_news(limit=10):
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id="app_server_group"
    )

    messages = []
    for msg in consumer:
        messages.append(msg.value)
        if len(messages) >= limit:
            break

    consumer.close()
    return messages