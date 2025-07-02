import time
import uuid

import redis.asyncio as aioredis

from food_co2_estimator.pydantic_models.response_models import JobResult, JobStatus

REDIS_EXPIRATION = 3600


class RedisCache:
    def __init__(self, redis_client: aioredis.Redis, expiration: int | None = None):
        self.redis_client = redis_client
        self.expiration = REDIS_EXPIRATION if expiration is None else expiration

    @classmethod
    async def create(cls, expiration: int | None = None):
        redis_client = aioredis.Redis(host="localhost", port=6379, db=0)
        return cls(redis_client, expiration)

    async def get(self, key: str):
        """
        Get the value from Redis cache.
        """
        value = await self.redis_client.get(key)
        if value is not None:
            return value

    async def set(self, key: str, value: str):
        """
        Set the value in Redis cache.
        """
        await self.redis_client.set(key, value, ex=self.expiration)

    async def update_job_status(
        self,
        uid: str,
        status: JobStatus,
        result: str | None = None,
    ):
        await self.set(
            uid,
            JobResult(status=status, result=result).model_dump_json(),
        )

    async def delete(self, key: str):
        """
        Delete the value from Redis cache.
        """
        await self.redis_client.delete(key)

    async def aclose(self):
        """
        Close the Redis connection.
        """
        await self.redis_client.aclose()

    async def clear(self):
        """
        Clear the Redis cache.
        """
        await self.redis_client.flushdb()

    async def check_rate_limit(
        self,
        ip: str,
        max_requests: int,
        window_seconds: int,
        api_key: str | None = None,
    ) -> tuple[bool, int]:
        """
        Check if the request should be rate limited, using a combination of api_key and IP address.
        Returns (is_allowed, remaining_requests)
        """
        if api_key:
            key = f"ratelimit:{api_key}:{ip}"
        else:
            key = f"ratelimit:{ip}"
        now_ms = int(time.time() * 1000)  # Current time in ms
        window_start = now_ms - (window_seconds * 1000)

        # Remove old requests outside the window
        await self.redis_client.zremrangebyscore(key, 0, window_start)

        # Count current requests in window
        current_requests = await self.redis_client.zcard(key)

        if current_requests >= max_requests:
            remaining = 0
            is_allowed = False
        else:
            # Add current request timestamp with a unique value
            unique_value = f"{now_ms}-{uuid.uuid4()}"
            await self.redis_client.zadd(key, {unique_value: now_ms})
            # Set expiration to ensure cleanup
            await self.redis_client.expire(key, window_seconds)
            remaining = max_requests - current_requests - 1
            is_allowed = True

        return is_allowed, remaining
