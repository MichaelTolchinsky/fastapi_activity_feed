from typing import AsyncGenerator
from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()
redis_client: Redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    yield redis_client
