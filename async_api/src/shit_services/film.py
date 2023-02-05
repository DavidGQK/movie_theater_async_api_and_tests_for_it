from collections import namedtuple
from functools import lru_cache
from typing import Dict

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from services.base import EndPointParam, MainService

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 min


class FilmService(MainService):
    index = "movies"
    model = Film

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_params["filter_genre"] = EndPointParam(
            parse_func=self._parse_filter_genre, required_params=("filter_genre")
        )

    def _parse_filter_genre(self, filter_genre: str) -> Dict[str, dict]:
        return "body", {
            "query": {
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {"must": [{"match": {f"genres.uuid": filter_genre}}]}
                    },
                }
            },
        }

    async def get_films(self, **end_point_params):
        searched_films = await self._search(
            filter_path=["hits.hits._id", "hits.hits" "._source"],
            **self._parse_params(**end_point_params),
        )
        return [self.model(**doc["_source"]) for doc in searched_films]


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
