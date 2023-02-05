import pytest
from testdata.genre_test_data import GENRE_BY_UUID_DATA, GENRE_DATA

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("genre_uuid,expected_status,expected_body", GENRE_BY_UUID_DATA)
async def test_genre_by_uuid(
    get_request, test_case_helper, genre_uuid, expected_status, expected_body
):
    """Test for obtaining information on genre by UUID"""
    response = await get_request(f"/genre/{genre_uuid}")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)


@pytest.mark.parametrize("expected_status,expected_body", GENRE_DATA)
async def test_genre_list(
    get_request, test_case_helper, expected_status, expected_body
):
    """Test for obtaining genres"""
    response = await get_request("/genre")

    assert response.status == expected_status
    test_case_helper.assertEqual(response.body, expected_body)
