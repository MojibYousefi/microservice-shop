import redis.asyncio as aioredis
from typing import AsyncGenerator
from backend.config.config import settings

# Global async redis connection pool
redis_client: aioredis.Redis = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    FastAPI dependency for accessing the async Redis client.
    """
    yield redis_client


async def close_redis() -> None:
    """
    Closes the async Redis client connection pool gracefully.
    """
    await redis_client.close()
