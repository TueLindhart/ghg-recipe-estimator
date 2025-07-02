# NOTE: app tests should be in test own separate folder / repository

from time import sleep

import pytest
from asgi_lifespan import LifespanManager
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app import RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW, app


@pytest.mark.skip(
    "Unsure about implementation details of rate limiting and if is provides any value"
)
@pytest.mark.asyncio
async def test_rate_limit():
    async with LifespanManager(app):
        redis_client = app.state.redis
        await redis_client.clear()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            for i in range(RATE_LIMIT_MAX_REQUESTS):
                resp = await ac.get("/comparison?kgco2=10")
                assert (
                    resp.status_code == 200
                ), f"Request {i+1} failed with status code {resp.status_code}"

            with pytest.raises(HTTPException):
                await ac.get("/comparison?kgco2=10")

            sleep(RATE_LIMIT_WINDOW + 1)
            resp = await ac.get("/comparison?kgco2=10")
            assert (
                resp.status_code == 200
            ), "Request after rate limit reset failed with status"
