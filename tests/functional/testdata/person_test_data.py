from collections import namedtuple
from http import HTTPStatus

# /person/{person_uuid}
PersonByUUIDCase = namedtuple(
    "PersonByUUIDCase", ("person_uuid", "expected_status", "expected_body")
)
PERSON_BY_UUID_DATA = [
    PersonByUUIDCase(
        person_uuid="96f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.OK,
        expected_body={
            "uuid": "96f18d84-55e0-4718-b87f-4a9e63544d76",
            "full_name": "George Germanetti",
            "films": [
                {
                    "uuid": "b164fef5-0867-46d8-b635-737e1721f6bf",
                    "title": "Tar with a Star",
                    "role": "director",
                }
            ],
        },
    ),
    PersonByUUIDCase(
        person_uuid="16f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.NOT_FOUND,
        expected_body={"detail": "Person not found"},
    ),
    PersonByUUIDCase(  # validation error
        person_uuid="not-uuid",
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "person_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

# /person/{person_uuid}/film
PersonFilmsByUUIDCase = namedtuple(
    "PersonFilmsByUUIDCase", ("person_uuid", "expected_status", "expected_body")
)
PERSON_FILMS_BY_UUID_DATA = [
    PersonFilmsByUUIDCase(
        person_uuid="96f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.OK,
        expected_body=[
            {
                "uuid": "b164fef5-0867-46d8-b635-737e1721f6bf",
                "title": "Tar with a Star",
                "role": "director",
            }
        ],
    ),
    PersonFilmsByUUIDCase(
        person_uuid="16f18d84-55e0-4718-b87f-4a9e63544d76",
        expected_status=HTTPStatus.NOT_FOUND,
        expected_body={"detail": "Person not found"},
    ),
    PersonFilmsByUUIDCase(  # validation error
        person_uuid="not-uuid",
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "person_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

# /person/search
PersonSearchCase = namedtuple(
    "PersonSearchCase", ("params", "expected_status", "expected_body")
)
PERSON_SEARCH_DATA = [
    PersonSearchCase(
        params={},
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["query", "query"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        },
    ),
    PersonSearchCase(
        params={"query": "bad_query"},
        expected_status=HTTPStatus.OK,
        expected_body=[],
    ),
    PersonSearchCase(
        params={"query": "george", "page[size]": 2, "page[number]": 5},
        expected_status=HTTPStatus.OK,
        expected_body=[
            {
                "uuid": "a57c7839-6af9-4f97-8899-ab29f193988e",
                "full_name": "George Nichols",
                "films": [
                    {
                        "uuid": "24eafcd7-1018-4951-9e17-583e2554ef0a",
                        "title": "The Star Boarder",
                        "role": "director",
                    }
                ],
            },
            {
                "uuid": "14946aea-53fe-4d06-986d-c888227a0ae9",
                "full_name": "George Stroumboulopoulos",
                "films": [
                    {
                        "uuid": "2f0b8fa3-8930-4046-bdcf-2f257899a2b9",
                        "title": "The One: Making a Music Star",
                        "role": "actor",
                    }
                ],
            },
        ],
    ),
]
