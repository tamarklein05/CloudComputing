import os
import json
import threading
import time
from kafka import KafkaProducer, KafkaConsumer

# main.py
# Simple Kafka link (producer + consumer) using kafka-python
# Install: pip install kafka-python


BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "test-topic")
GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "my-group")


def create_producer(bootstrap_servers: str = BOOTSTRAP) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else None,
        retries=5,
    )


def create_consumer(
    topic: str = TOPIC,
    group_id: str = GROUP,
    bootstrap_servers: str = BOOTSTRAP,
    auto_offset_reset: str = "earliest",
) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda b: json.loads(b.decode("utf-8")) if b is not None else None,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=True,
    )


def send_message(producer: KafkaProducer, topic: str, value, key: str | None = None):
    future = producer.send(topic, key=key, value=value)
    # block until the message is sent (or raise)
    record_metadata = future.get(timeout=10)
    return record_metadata


def consume_loop(consumer: KafkaConsumer, stop_event: threading.Event):
    try:
        for msg in consumer:
            print(f"consumed: topic={msg.topic} partition={msg.partition} offset={msg.offset} key={msg.key} value={msg.value}")
            if stop_event.is_set():
                break
    finally:
        consumer.close()


if __name__ == "__main__":
    producer = create_producer()
    consumer = create_consumer()

    stop_event = threading.Event()
    t = threading.Thread(target=consume_loop, args=(consumer, stop_event), daemon=True)
    t.start()

    try:
        # send a few test messages
        for i in range(3):
            meta = send_message(producer, TOPIC, {"i": i, "text": f"hello {i}"}, key=str(i))
            print(f"sent: topic={meta.topic} partition={meta.partition} offset={meta.offset}")
            time.sleep(0.5)
    finally:
        # allow consumer to finish printing, then stop
        time.sleep(1)
        stop_event.set()
        producer.flush()
        producer.close()