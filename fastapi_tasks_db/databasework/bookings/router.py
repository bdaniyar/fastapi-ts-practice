from fastapi import APIRouter
from sqlalchemy import select
from fastapi_tasks_db.databasework.bookings.dao import BookingDAO
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.bookings.m import Bookings
router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("/{id}")
async def get_bookings():
    return await BookingDAO.find_one_or_more(rooms_id=1)
