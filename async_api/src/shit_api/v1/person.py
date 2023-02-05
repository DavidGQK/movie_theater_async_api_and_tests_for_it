import asyncio
import sys
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

sys.path.append("/code/models")
sys.path.append("/code/services")
from typing import List

from models.person import PersonRole
from services.person import PersonService, get_person_service

router = APIRouter()


class PersonFilm(BaseModel):
    uuid: UUID
    title: str
    role: PersonRole


class Person(BaseModel):
    uuid: UUID
    full_name: str
    films: List[PersonFilm] = []


@router.get("/search", response_model=List[Person], summary="Search by person")
async def person_search(
    query: str,
    page_number: int = Query(1, alias="page[number]"),
    page_size: int = Query(25, alias="page[size]"),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    """
    Available for withdrawal:
    - **query**: request
    - **page[number]**: requested page
    - **page[size]**: page size
    Check me: http://localhost:8000/api/v1/person/search?query=george&page[number]=0&page[size]=5
    """

    persons = await person_service.get_by_full_name(
        query_full_name=query, page_number=page_number - 1, page_size=page_size
    )

    films_of_persons = await asyncio.gather(
        *[person_service.get_films_by_person_uuid(person.uuid) for person in persons]
    )
    for person, films in zip(persons, films_of_persons):
        person.films = films

    return [
        Person(uuid=person.uuid, full_name=person.full_name, films=person.films)
        for person in persons
    ]


@router.get("/{person_uuid}/film", summary="Movie output for a person")
async def person_films(
    person_uuid: UUID,
    person_service: PersonService = Depends(get_person_service),
) -> List[PersonFilm]:
    """
    Displaying information about a movie by person's uuid:
    - **person_uuid**: required field
    Check me: http://localhost:8000/api/v1/person/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/film
    """
    print("PERSSSSSSSSON ID FIIIIIIIIIIIIIILM")
    person = await person_service.get_by_uuid(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    person_films = await person_service.get_films_by_person_uuid(person_uuid)

    return [
        PersonFilm(uuid=film.uuid, title=film.title, role=film.role)
        for film in person_films
    ]


@router.get(
    "/{person_uuid}",
    response_model=Person,
    summary="Detailed information about the person",
)
async def person_details(
    person_uuid: UUID, person_service: PersonService = Depends(get_person_service)
) -> Person:
    """
    Displaying information about a person by uuid:
    - **person_uuid**: required field
    Check me: http://localhost:8000/api/v1/person/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a
    """

    person = await person_service.get_by_uuid(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    person_films = await person_service.get_films_by_person_uuid(person_uuid)

    return Person(uuid=person.uuid, full_name=person.full_name, films=person_films)
