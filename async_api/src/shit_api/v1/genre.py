import sys
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

sys.path.append("/code/models")
sys.path.append("/code/services")
from typing import Dict, List

from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()

genres = Optional[List[Dict[str, str]]]


async def get_genres(
    genres_service: GenreService = Depends(get_genre_service),
    page_number: int = 0,
    page_size: int = 50,
):
    genres = await genres_service.get_genres(
        page_number=page_number,
        page_size=page_size,
    )
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="not one genre found"
        )
    return genres


@router.get("/", summary="List of genres")
async def genres_list(
    genres_service: GenreService = Depends(get_genre_service),
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(50, alias="page[size]"),
) -> List[Genre]:
    """
    The following parameters could be set:
    - **page[number]**: requested page
    - **page[size]**: page size
    """
    print("GEEEEEEEEEEEEEEEEEEEEEENREEEEEEEEEEEEEEEEEEES")
    return await get_genres(
        genres_service=genres_service,
        page_number=page_number - 1,
        page_size=page_size,
    )


@router.get("/{genre_uuid}", summary="Genre search by uuid")
async def genre_details(
    genre_uuid: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Optional[Genre]:
    """
    Required field:
    - **genre_uuid**: genre uuid
    """
    genre = await genre_service.get_by_uuid(uuid=genre_uuid)
    if genre:
        return genre
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
