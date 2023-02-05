import asyncio
from dataclasses import dataclass
from unittest import TestCase

import aiohttp
import pytest
from multidict import CIMultiDictProxy
from settings import get_settings
from utils.connections import elastic_connect, redis_connect
from utils.setup import elastic_setup, redis_setup


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def test_case_helper():
    # For functions like .assertEqual().
    # It allows compare objects with complex structure
    return TestCase()


@pytest.fixture(scope="session", autouse=get_settings().should_wait_refresh)
async def elastic_client(settings):
    """Connection setup and setting of Elastic client"""
    client = await elastic_connect(host=settings.es_host)

    await elastic_setup(es_client=client)

    yield client
    await client.close()


@pytest.fixture(scope="session", autouse=get_settings().should_wait_refresh)
async def redis_client(settings):
    """Connection setup and setting of Redis client"""
    client = await redis_connect(host=settings.redis_host, port=settings.redis_port)

    await redis_setup(redis_client=client)

    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def get_request(session, settings):
    async def inner(path: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        async_api_host = settings.async_api_host
        # export ASYNC_API_HOST="http:// 0.0.0.0:8000/api/v1
        # python -m pytest -vv
        url = f"{async_api_host}{path}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
