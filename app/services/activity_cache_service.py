import logging
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from typing import List
from app.core.config import get_settings
from app.core.redis import get_redis_client
from app.dtos.activity_response_dto import ActivityResponseDTO
import json

settings = get_settings()
logger = logging.getLogger(__name__)


class ActivityCacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_user_activities(self, user_id: int) -> List[ActivityResponseDTO] | None:
        cached = await self.redis.get(f"user_feed:{user_id}")
        if cached:
            logger.info(f"Cache hit for user feed: {user_id}")
            data = json.loads(cached)
            return [ActivityResponseDTO(**item) for item in data]
        logger.info(f"Cache miss for user feed: {user_id}")
        return None

    async def set_user_activities(
        self, user_id: int, feed: List[ActivityResponseDTO], ttl: int = settings.REDIS_TTL
    ) -> None:
        payload = [jsonable_encoder(dto) for dto in feed]
        await self.redis.set(f"user_feed:{user_id}", json.dumps(payload), ex=ttl)


def get_activity_cache_service(redis: Redis = Depends(get_redis_client)) -> ActivityCacheService:
    return ActivityCacheService(redis)
