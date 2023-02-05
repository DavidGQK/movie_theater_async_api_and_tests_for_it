from functools import lru_cache

from pydantic import BaseSettings, Field

CONNECTIONS_MAX_TIME = 60

ES_SCHEMA_FILE = "testdata/indexes/schema.json"
ES_INDEXES_FILES = (
    ("movies", "testdata/indexes/movies.json"),
    ("genres", "testdata/indexes/genres.json"),
    ("persons", "testdata/indexes/persons.json"),
)


class Settings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="ES_HOST")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    async_api_host: str = Field("http://127.0.0.1:8000/api/v1", env="ASYNC_API_HOST")
    should_wait_refresh: bool = Field(True, env="SHOULD_WAIT_REFRESH")


@lru_cache
def get_settings():
    return Settings()
