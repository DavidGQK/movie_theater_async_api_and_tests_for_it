import asyncio
import logging

import aioredis
import backoff
from elasticsearch import AsyncElasticsearch
from settings import CONNECTIONS_MAX_TIME, Settings


def backoff_handler(details):
    logging.error(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=CONNECTIONS_MAX_TIME,
)
async def redis_connect(*, host: str, port: int) -> aioredis.Redis:
    redis = await aioredis.create_redis(f"redis://{host}:{port}")
    pong = await redis.ping()
    if not pong:
        raise ConnectionError("Connection failed")
    return redis


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=CONNECTIONS_MAX_TIME,
)
async def elastic_connect(*, host: str) -> AsyncElasticsearch:
    elastic = AsyncElasticsearch(hosts=host, verify_certs=True)
    if not await elastic.ping():
        raise ConnectionError("Connection failed")
    return elastic


async def main():
    """Waiters for Elasticsearch, REDIS"""
    settings = Settings()
    es = await elastic_connect(host=settings.es_host)
    await es.close()

    redis = await redis_connect(host=settings.redis_host, port=settings.redis_port)
    redis.close()
    await redis.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
