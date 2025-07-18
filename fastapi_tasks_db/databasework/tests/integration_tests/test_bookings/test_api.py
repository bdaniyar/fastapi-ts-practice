import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "rooms_id, date_from, date_to, status_code",
    [
        *[(3, "2030-05-01", "2030-05-15", 200)] * 8,
        (3, "2030-05-01", "2030-05-15", 409),
        (3, "2030-05-01", "2030-05-15", 409),
    ],
)
async def test_add_and_get_booking(
    rooms_id, date_from, date_to, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/bookings",
        params={
            "rooms_id": rooms_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
