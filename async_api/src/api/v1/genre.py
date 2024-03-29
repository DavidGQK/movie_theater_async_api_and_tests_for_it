from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()

genres = Optional[List[Dict[str, str]]]


@router.get("/")
async def genre_list(
    genre_service: GenreService = Depends(get_genre_service),
) -> List[Genre]:
    return await genre_service.genre_list()


@router.get("/{genre_uuid}")
async def genre_details(
    genre_uuid: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Optional[Genre]:
    genre = await genre_service.get_by_uuid(uuid=genre_uuid)
    if genre:
        return genre
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
