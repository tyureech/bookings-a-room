import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id, date_from, date_to, price, book_rooms, status_code",
    [
        (4, "2012-12-10", "2012-12-19", 123, 1, 201),
        (4, "2012-12-19", "2012-12-10", 123, 1, 400),
        (4, "2012-12-10", "2012-12-19", 123, 2, 201),
        (4, "2012-12-10", "2012-12-19", 123, 3, 201),
        (4, "2012-12-10", "2012-12-19", 123, 4, 201),
        (4, "2012-12-10", "2012-12-19", 123, 5, 201),
        (4, "2012-12-10", "2012-12-19", 123, 5, 409),
        (0, "2012-12-10", "2012-12-19", 123, 5, 404),
    ],
)
async def test_add_and_get_user_bookings(
    room_id: int,
    date_from: str,
    date_to: str,
    price: int,
    book_rooms: int,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    add_booking = await authenticated_ac.post(
        url="/bookings/add",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "price": price,
        },
    )
    assert add_booking.status_code == status_code

    user_bookings = await authenticated_ac.get(url="/bookings/user")
    count_bookings = len(user_bookings.json())
    assert count_bookings == book_rooms


async def test_get_and_delete_all_bookings(authenticated_ac: AsyncClient):
    all_bookings = await authenticated_ac.get(url="/bookings")
    assert all_bookings.status_code == 200

    count = len(all_bookings.json())
    for sequence_number in range(1, count + 1):
        res = await authenticated_ac.delete(f"/bookings/{sequence_number}")
        res.status_code == 204

    all_bookings = await authenticated_ac.get(url="/bookings")
    assert len(all_bookings.json()) == 0
