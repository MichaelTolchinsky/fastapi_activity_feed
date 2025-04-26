from aiokafka import AIOKafkaProducer
from app.core.config import get_settings

settings = get_settings()

_kafka_producer: AIOKafkaProducer | None = None


async def get_kafka_producer() -> AIOKafkaProducer:
    global _kafka_producer
    if _kafka_producer is None:
        _kafka_producer = AIOKafkaProducer(bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}")
        await _kafka_producer.start()
    return _kafka_producer


async def close_kafka_producer():
    global _kafka_producer
    if _kafka_producer:
        await _kafka_producer.stop()
