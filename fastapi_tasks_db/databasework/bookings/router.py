from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from fastapi_tasks_db.databasework.bookings.dao import BookingDAO
from fastapi_tasks_db.databasework.bookings.schemas import SBooking
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.hotels.schemas import SBookingInfo
from fastapi_tasks_db.databasework.tasks.tasks import \
    send_booking_confirmation_email
from fastapi_tasks_db.databasework.users.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user=Depends(get_current_user)):  # -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    background_tasks: BackgroundTasks,
    rooms_id: int,
    date_from: date,
    date_to: date,
    user=Depends(get_current_user),
):
    booking = await BookingDAO.add_booking(user.id, rooms_id, date_from, date_to)
    if not booking:
        raise HTTPException(status_code=409, detail="Booking could not be created")
    booking_dict = SBooking.model_validate(booking).model_dump()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict


@router.get("", response_model=list[SBookingInfo])
async def get_user_bookings(user=Depends(get_current_user)):
    bookings = await BookingDAO.get_bookings_with_room_info(user.id)
    return [
        SBookingInfo(
            room_id=b.room_id,
            user_id=b.user_id,
            date_from=b.date_from,
            date_to=b.date_to,
            price=price,
            total_cost=total_cost,
            total_days=total_days,
            image_id=image_id,
            name=name,
            description=description,
            services=services,
        )
        for b, image_id, name, description, services, price, total_days, total_cost in bookings
    ]


@router.delete("/{booking_id}", status_code=204)
async def delete_booking(booking_id: int, user=Depends(get_current_user)):
    deleted = await BookingDAO.delete_by_id(booking_id, user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено или недоступно для удаления",
        )
