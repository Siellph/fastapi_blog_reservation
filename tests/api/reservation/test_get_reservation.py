from pathlib import Path

import pytest
from dateutil.parser import parse
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'id',
        'user_id',
        'restaurant_id',
        'date_reserv',
        'guest_count',
        'comment',
        'responce_status',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'user',
            'qwerty',
            2,
            2,
            1,
            '2024-03-03T11:30:57.390Z',
            2,
            'Особые требования к столику',
            False,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.reservation.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_reservation(
    client: AsyncClient,
    username: str,
    password: str,
    id: int,
    user_id: int,
    restaurant_id: int,
    date_reserv: str,
    guest_count: int,
    comment: str,
    responce_status: bool,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['reservation']['get_put_delete'].format(reservation_id=id),
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        response_data = response.json()
        assert response_data['id'] == id
        assert response_data['user_id'] == user_id
        assert response_data['restaurant_id'] == restaurant_id
        assert parse(response_data['date_reserv']) == parse(date_reserv)
        assert response_data['guest_count'] == guest_count
        assert response_data['comment'] == comment
        assert response_data['status'] == responce_status
