from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from fastapi_tasks_db.databasework.bookings.dao import BookingDAO
from fastapi_tasks_db.databasework.bookings.schemas import SBooking
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.bookings.m import Bookings
from typing import List

from fastapi_tasks_db.databasework.users.dependencies import get_current_user
from fastapi_tasks_db.databasework.users.users import Users
router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)