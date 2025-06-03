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
