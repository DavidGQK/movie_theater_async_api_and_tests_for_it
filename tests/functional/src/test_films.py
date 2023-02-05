import pytest
from testdata.films_test_data import (FILM_BY_UUID_DATA, FILM_SEARCH_DATA,
                                      FILMS_GENRES, FILMS_LEN_PAGES_PARAMS,
                                      FILMS_PAGES_PARAMS, FILMS_SORTING_PARAMS)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("film_uuid,expected_status,expected_body", FILM_BY_UUID_DATA)
async def test_film_by_uuid(
    get_request, test_case_helper, film_uuid, expected_status, expected_body
):
    response = await get_request(f"/film/{film_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("params,expected_status,expected_body", FILM_SEARCH_DATA)
async def test_film_search(
    get_request, test_case_helper, params, expected_status, expected_body
):
    response = await get_request("/film/search", params=params)

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("sorting,expected_status,expected_body", FILMS_SORTING_PARAMS)
async def test_film_imdb_sorting(
    get_request, test_case_helper, sorting, expected_body, expected_status
):
    response = await get_request(f"/film", {"sort": sorting, "page[size]": 2})

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize(
    "page_number, expected_response_status, expected_body", FILMS_PAGES_PARAMS
)
async def test_film_pages(
    get_request, test_case_helper, page_number, expected_response_status, expected_body
):
    response = await get_request(
        f"/film", {"page[number]": page_number, "page[size]": 2}
    )

    assert response.status == expected_response_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize(
    "page_number, page_len, expected_response_status", FILMS_LEN_PAGES_PARAMS
)
async def test_film_len_pages(
    get_request, page_number, page_len, expected_response_status
):
    response = await get_request(f"/film", {"page[size]": page_number})

    assert response.status == expected_response_status
    assert len(response.body) == page_len


@pytest.mark.parametrize("genre_uuid, expected_response_status", FILMS_GENRES)
async def test_film_genre_sort(get_request, genre_uuid, expected_response_status):
    response = await get_request(f"/film", {"filter[genre]": genre_uuid})

    assert response.status == expected_response_status
