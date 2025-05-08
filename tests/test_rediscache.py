import json

import pytest

from food_co2_estimator.pydantic_models.response_models import JobStatus
from food_co2_estimator.rediscache import RedisCache


class MockCache:
    def __init__(self):
        self.cache = {}

    async def get(self, key: str):
        return self.cache.get(key)

    async def set(self, key: str, value: str, ex=None):
        self.cache[key] = value

    async def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    async def flushdb(self):
        self.cache.clear()


class MockRedisCache(RedisCache):
    def __init__(self, *args, **kwargs):
        self.redis_client = MockCache()
        self.expiration = 1


# Fixture to monkey-patch the aioredis.Redis class to return our FakeRedis.
@pytest.fixture
def mock_redis():
    return MockRedisCache()


@pytest.mark.asyncio
async def test_set_and_get(mock_redis: MockRedisCache):
    key = "test_key"
    value = "test_value"
    await mock_redis.set(key, value)
    retrieved = await mock_redis.get(key)
    assert retrieved == value


@pytest.mark.asyncio
async def test_delete_key(mock_redis: MockRedisCache):
    key = "delete_key"
    value = "some_value"
    await mock_redis.set(key, value)
    await mock_redis.delete(key)
    retrieved = await mock_redis.get(key)
    assert retrieved is None


@pytest.mark.asyncio
async def test_clear_cache(mock_redis: MockRedisCache):
    # Set a few keys in the cache.
    keys = ["a", "b", "c"]
    for key in keys:
        await mock_redis.set(key, f"value_{key}")

    # Clear the cache.
    await mock_redis.clear()

    # Check that no key returns a value.
    for key in keys:
        retrieved = await mock_redis.get(key)
        assert retrieved is None


@pytest.mark.asyncio
async def test_update_job_status(mock_redis: MockRedisCache):
    uid = "job_1"
    # Assuming JobStatus can be constructed with a string (e.g., "completed")
    status = JobStatus("Completed")
    result = "success"

    await mock_redis.update_job_status(uid, status, result)
    stored_json = await mock_redis.get(uid)

    # The stored value is a JSON string from JobResult.model_dump_json()
    data = json.loads(stored_json)  # type: ignore
    assert data["status"] == JobStatus.COMPLETED
    assert data["result"] == result
