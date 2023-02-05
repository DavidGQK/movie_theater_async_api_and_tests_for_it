from collections import namedtuple
from http import HTTPStatus

# /genre/{genre_uuid}
GenreByUUIDCase = namedtuple(
    "GenreByUUIDCase", ("genre_uuid", "expected_status", "expected_body")
)
GENRE_BY_UUID_DATA = [
    GenreByUUIDCase(
        genre_uuid="6c162475-c7ed-4461-9184-001ef3d9f26e",
        expected_status=HTTPStatus.OK,
        expected_body={
            "uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e",
            "name": "Sci-Fi",
        },
    ),
    GenreByUUIDCase(
        genre_uuid="0c162471-c7ed-4461-9184-001af3d9f26e",
        expected_status=HTTPStatus.NOT_FOUND,
        expected_body={"detail": "genre not found"},
    ),
    GenreByUUIDCase(  # validation error
        genre_uuid="not-uuid",
        expected_status=HTTPStatus.UNPROCESSABLE_ENTITY,
        expected_body={
            "detail": [
                {
                    "loc": ["path", "genre_uuid"],
                    "msg": "value is not a valid uuid",
                    "type": "type_error.uuid",
                }
            ]
        },
    ),
]

# /genre
GenresCase = namedtuple("GenresCase", ("expected_status", "expected_body"))
GENRE_DATA = [
    GenresCase(
        expected_status=HTTPStatus.OK,
        expected_body=[
            {"uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            {"uuid": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
            {"uuid": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
            {"uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
            {"uuid": "1cacff68-643e-4ddd-8f57-84b62538081a", "name": "Drama"},
            {"uuid": "56b541ab-4d66-4021-8708-397762bff2d4", "name": "Music"},
            {"uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
            {"uuid": "526769d7-df18-4661-9aa6-49ed24e9dfd8", "name": "Thriller"},
            {"uuid": "ca88141b-a6b4-450d-bbc3-efa940e4953f", "name": "Mystery"},
            {"uuid": "5373d043-3f41-4ea8-9947-4b746c601bbd", "name": "Comedy"},
        ],
    ),
]