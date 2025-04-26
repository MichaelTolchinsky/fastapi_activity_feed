import json
from aiokafka import AIOKafkaProducer
from fastapi import Depends

from app.core.kafka import get_kafka_producer
from app.core.logging_utils import get_logger

logger = get_logger(__name__)


class KafkaProducerService:
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def send(self, topic: str, message: dict) -> None:
        try:
            payload = json.dumps(message).encode("utf-8")
            await self._producer.send_and_wait(topic, payload)
            logger.info(f"✅ Sent message to Kafka topic {topic}")
        except Exception as e:
            logger.error(f"❌ Failed to send message to Kafka: {e}")


async def get_kafka_producer_service(producer: AIOKafkaProducer = Depends(get_kafka_producer)) -> KafkaProducerService:
    return KafkaProducerService(producer)
