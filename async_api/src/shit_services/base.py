import logging
from collections import namedtuple
from http import HTTPStatus
from typing import Dict
from uuid import UUID

from aiocache import cached
from db.redis import get_redis_cache_config
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
from fastapi import HTTPException
from pydantic import BaseModel

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 min
EndPointParam = namedtuple("EndPointParam", ("parse_func", "required_params"))


class MainService:
    # Definition of base model and index
    model = BaseModel
    index = ""

    # Class initialization, settings for redis и elastic
    def __init__(self, elastic: AsyncElasticsearch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elastic = elastic

        # Definition accessible params for endpoints
        self.valid_params = {
            "sort": EndPointParam(
                parse_func=self._parse_sort, required_params=("sort",)
            ),
            "page_number": EndPointParam(
                parse_func=self._parse_page_number,
                required_params=("page_number", "page_size"),
            ),
            "page_size": EndPointParam(
                parse_func=self._parse_page_size, required_params=("page_size",)
            ),
            "query": EndPointParam(
                parse_func=self._parse_query, required_params=("query")
            ),
        }

    def _parse_sort(self, sort: str) -> Dict[str, str]:
        sort_direction = "desc" if sort.startswith("-") else "asc"
        sort_field = sort.removeprefix("-")
        return "sort", f"{sort_field}:{sort_direction}"

    def _parse_query(self, query: str) -> Dict[str, str]:
        return "body", {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description"],
                    "type": "best_fields",
                }
            },
        }

    def _parse_page_number(self, page_number, page_size) -> Dict[str, int]:
        return "from_", page_number * page_size

    def _parse_page_size(self, page_size) -> Dict[str, int]:
        return "size", page_size

    # Genera params parser
    def _parse_params(self, **end_point_params):
        # By default search everything
        result_params = {"body": {"query": {"match_all": {}}}}

        for end_point_param in end_point_params:
            if end_point_param in self.valid_params:
                param_name, param_value = self.valid_params[end_point_param].parse_func(
                    **{
                        param: value
                        for param, value in end_point_params.items()
                        if param in self.valid_params[end_point_param].required_params
                    }
                )
                result_params[param_name] = param_value

        return result_params

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_config(),
    )
    async def get_by_uuid(self, uuid: UUID):
        result_object = {}
        try:
            doc_ = await self.elastic.get(index=self.index, id=str(uuid))
            result_object = self.model(**doc_["_source"])

        except (RequestError, NotFoundError):
            logging.exception(
                "Elasticsearch error has been raised while getting by UUID"
            )
        finally:
            return result_object

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_config(),
    )
    async def _search(self, index: str = None, **search_options):
        index = index or self.index
        result_objects = []
        try:
            response = await self.elastic.search(index=index, **search_options)
            if response:
                result_objects = response["hits"]["hits"]
        except (RequestError, NotFoundError) as elastic_error:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=elastic_error.info["error"]["root_cause"][0]["reason"],
            )
        return
