# NOTE: app tests should be in test own separate folder / repository

import pytest
from asgi_lifespan import LifespanManager
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app import RATE_LIMIT_MAX_REQUESTS, app


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

            with pytest.raises(HTTPException) as exc_info:
                await ac.get("/comparison?kgco2=10")
