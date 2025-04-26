import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer

from app.core.config import get_settings
from app.core.logging_utils import get_logger
from app.core.redis import get_redis_client
from app.dtos.activity_response_dto import ActivityResponseDTO
from app.services.activity_cache_service import ActivityCacheService


settings = get_settings()
logger = get_logger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        "activity.created",
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        group_id="activity-feed-consumer-group",
        auto_offset_reset="earliest",
    )

    await consumer.start()
    logger.info("Kafka consumer started, listening to activity.created topic")

    redis_client = await get_redis_client()
    cache_service = ActivityCacheService(redis_client)

    try:
        async for msg in consumer:
            try:
                payload = json.loads(msg.value.decode("utf-8"))
                logger.info(f"Received message: {payload}")

                await handle_activity_created(payload, cache_service)
            except Exception as e:
                logger.error(f"Failed to process message: {e}")

    finally:
        await consumer.stop()


async def handle_activity_created(payload: dict, cache_service: ActivityCacheService) -> None:
    new_activity = ActivityResponseDTO(**payload)
    user_id = new_activity.user_id

    # Get existing user feed (if exists)
    existing_feed = await cache_service.get_user_activities(user_id) or []
    # Insert new activity at the beginning
    updated_feed = [new_activity] + existing_feed
    # Save updated feed back to Redis
    await cache_service.set_user_activities(user_id, updated_feed)

    logger.info(f"Updated Redis feed cache for user {user_id}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(consume())
