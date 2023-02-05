import pytest
from testdata.person_test_data import (PERSON_BY_UUID_DATA,
                                       PERSON_FILMS_BY_UUID_DATA,
                                       PERSON_SEARCH_DATA)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "person_uuid,expected_status,expected_body", PERSON_BY_UUID_DATA
)
async def test_person_by_uuid(
    get_request, test_case_helper, person_uuid, expected_status, expected_body
):
    """Test for obtaining information on person by UUID"""
    response = await get_request(f"/person/{person_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize(
    "person_uuid,expected_status,expected_body", PERSON_FILMS_BY_UUID_DATA
)
async def test_person_films_by_uuid(
    get_request, test_case_helper, person_uuid, expected_status, expected_body
):
    """Test for obtaining movies by person's UUID"""
    response = await get_request(f"/person/{person_uuid}/film")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("params,expected_status,expected_body", PERSON_SEARCH_DATA)
async def test_person_search(
    get_request, test_case_helper, params, expected_status, expected_body
):
    """Test for persons search"""
    response = await get_request("/person/search", params=params)

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)
