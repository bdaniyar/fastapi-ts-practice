from datetime import date

from fastapi_tasks_db.databasework.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add_booking(
        user_id=2, rooms_id=2, date_from=date(2023, 7, 10), date_to=date(2023, 7, 24)
    )

    assert new_booking.user_id == 2
    assert new_booking.rooms_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None
