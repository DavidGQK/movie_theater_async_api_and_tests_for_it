import asyncio
import logging
from functools import lru_cache
from typing import Dict, List
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.person import Person, PersonFilm, PersonRole
from services.base import EndPointParam, MainService
from services.film import FilmService

PERSON_REDIS_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 min

logger = logging.getLogger(__name__)


class PersonService(MainService):
    model = Person
    index = "persons"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_params["query_full_name"] = EndPointParam(
            parse_func=self._parse_query_full_name, required_params=("query_full_name",)
        )

    def _parse_query_full_name(self, query_full_name: str) -> Dict[str, str]:
        return "body", {
            "query": {
                "match": {"full_name": {"query": query_full_name, "fuzziness": "auto"}}
            },
        }

    async def get_by_full_name(self, **end_point_params) -> List[Person]:
        persons = await self._search(
            filter_path=["hits.hits._source"],
            **self._parse_params(**end_point_params),
        )
        return [self.model(**doc["_source"]) for doc in persons]

    async def get_films_by_person_uuid(self, person_uuid: UUID) -> List[PersonFilm]:
        films_as_actor, films_as_writer, films_as_director = await asyncio.gather(
            self.get_films_by_role(
                person_uuid=person_uuid, elastic_path="actors", role=PersonRole.actor
            ),
            self.get_films_by_role(
                person_uuid=person_uuid, elastic_path="writers", role=PersonRole.writer
            ),
            self.get_films_by_role(
                person_uuid=person_uuid,
                elastic_path="directors",
                role=PersonRole.director,
            ),
        )
        films = films_as_actor + films_as_writer + films_as_director
        return films

    async def get_films_by_role(
        self, *, person_uuid: UUID, elastic_path: str, role: PersonRole
    ) -> List[PersonFilm]:
        films = await self._search(
            index=FilmService.index,
            query={
                "nested": {
                    "path": elastic_path,
                    "query": {
                        "bool": {
                            "must": [{"match": {f"{elastic_path}.uuid": person_uuid}}]
                        }
                    },
                }
            },
            fields=["hits.hits._source.uuid", "hits.hits._source.title"],
        )
        return [PersonFilm(role=role, **film["_source"]) for film in films]


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic)
