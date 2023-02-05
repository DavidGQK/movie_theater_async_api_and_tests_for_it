from functools import lru_cache
from typing import List

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import Genre
from services.base import MainService


class GenreService(MainService):
    index = "genres"
    model = Genre

    async def genre_list(self) -> List[Genre]:
        searched_genres = await self._search(query={"match_all": {}})
        return [self.model(**doc["_source"]) for doc in searched_genres]


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
