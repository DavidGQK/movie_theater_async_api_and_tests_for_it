import sys
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

sys.path.append("/code/models")
sys.path.append("/code/services")
from typing import Dict, List

from models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()

persons = Optional[List[Dict[str, str]]]


async def get_films(film_service: FilmService, **end_point_params):
    films = await film_service.get_films(
        **{key: value for key, value in end_point_params.items() if value}
    )

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="not one film found"
        )

    return [
        {
            "uuid": film.uuid,
            "title": film.title,
            "imdb_rating": film.imdb_rating,
        }
        for film in films
    ]


@router.get(
    "/",
    summary="List of movies",
)
async def films_list(
    film_service: FilmService = Depends(get_film_service),
    filter_genre: Optional[str] = Query(None, alias="filter[genre]"),
    sort: Optional[str] = Query(
        default="-imdb_rating", regex="^-?[a-zA-Z_]+$", alias="sort"
    ),
    page_number: int = Query(default=1, alias="page[number]"),
    page_size: int = Query(default=50, alias="page[size]"),
) -> List[dict]:
    """
    Available for withdrawal:
    - **filter[genre]**: sort by genre uuid
    - **sort**: sorted by rating -imdb_rating/imdb_rating
    - **page[number]**: requested page
    - **page[size]**: page size
    """
    return await get_films(
        film_service=film_service,
        sort=sort,
        filter_genre=filter_genre,
        page_size=page_size,
        page_number=page_number - 1,
    )


@router.get(
    "/search",
    summary="Movies search",
)
async def films_search(
    film_service: FilmService = Depends(get_film_service),
    sort: Optional[str] = Query(None, regex="^-?[a-zA-Z_]+$", alias="sort"),
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(50, alias="page[size]"),
    query: Optional[str] = Query(
        None,
        alias="query",
    ),
) -> List[dict]:
    """
    Available for withdrawal:
    - **query**: request
    - **sort**: sorted by rating -imdb_rating/imdb_rating
    - **page[number]**: requested page
    - **page[size]**: page size
    """
    return await get_films(
        film_service=film_service,
        sort=sort,
        query=query,
        page_number=page_number - 1,
        page_size=page_size,
    )


@router.get(
    "/{film_uuid}",
    response_model=Film,
    summary="Moview Details",
)
async def film_details(
    film_uuid: UUID,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    """
    Displaying information about a movie by uuid:
    - **film_uuid**: required field
    """
    print("MOVVVVVVVVVVVVIES")
    film = await film_service.get_by_uuid(uuid=film_uuid)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film.parse_obj(film)
