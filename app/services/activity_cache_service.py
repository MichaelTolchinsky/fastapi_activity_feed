import logging
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from typing import List
from app.core.config import get_settings
from app.core.logging_utils import get_logger
from app.core.redis import get_redis_client
from app.dtos.activity_response_dto import ActivityResponseDTO
import json

settings = get_settings()
logger = get_logger(__name__)


class ActivityCacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_user_activities(self, user_id: int) -> List[ActivityResponseDTO] | None:
        key = f"user_feed:{user_id}"
        try:
            cached = await self.redis.get(key)
            if cached:
                logger.info(f"Cache hit for user feed: {user_id}")
                data = json.loads(cached)
                return [ActivityResponseDTO(**item) for item in data]
            logger.info(f"Cache miss for user feed: {user_id}")
        except Exception as e:
            logger.error(f"Error accessing Redis for key {key}: {e}")
        return None

    async def set_user_activities(
        self, user_id: int, feed: List[ActivityResponseDTO], ttl: int = settings.REDIS_TTL
    ) -> None:
        key = f"user_feed:{user_id}"
        payload = [jsonable_encoder(dto) for dto in feed]
        try:
            await self.redis.set(key, json.dumps(payload), ex=ttl)
            logger.info(f"Successfully cached activities for user {user_id} with TTL {ttl} seconds.")
        except Exception as e:
            logger.error(f"Failed to cache activities for user {user_id}: {e}")


def get_activity_cache_service(redis: Redis = Depends(get_redis_client)) -> ActivityCacheService:
    return ActivityCacheService(redis)
