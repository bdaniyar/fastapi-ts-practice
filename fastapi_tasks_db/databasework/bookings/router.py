from datetime import date
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from fastapi_tasks_db.databasework.bookings.dao import BookingDAO
from fastapi_tasks_db.databasework.bookings.schemas import SBooking
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.bookings.m import Bookings
from typing import List
from fastapi_tasks_db.databasework.exceptions import RoomCannotBeBooked
from fastapi_tasks_db.databasework.users.dependencies import get_current_user
from fastapi_tasks_db.databasework.users.users import Users
router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(
    rooms_id:int, date_from:date, date_to:date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, rooms_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked