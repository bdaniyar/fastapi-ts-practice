from sqlalchemy import select
from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.dao.base import BaseDAO
from fastapi_tasks_db.databasework.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings