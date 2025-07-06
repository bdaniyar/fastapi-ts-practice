from datetime import date
from sqlalchemy import select, func, and_
from fastapi_tasks_db.databasework.hotels.models import Hotels, Rooms
from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.dao.base import BaseDAO
from sqlalchemy.orm import joinedload

class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_available_by_location_and_dates(cls, location: str, date_from, date_to):
        async with async_session_maker() as session:
            # Подзапрос: количество бронирований на каждый номер
            booked_rooms_subq = (
                select(
                    Bookings.rooms_id,
                    func.count(Bookings.id).label("booked_count")
                )
                .where(
                    and_(
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                )
                .group_by(Bookings.rooms_id)
                .subquery()
            )

            # Основной запрос: отели, где есть комнаты с оставшимися местами
            query = (
                select(Hotels)
                .options(joinedload(Hotels.rooms))
                .where(Hotels.location.ilike(f"%{location}%"))
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(booked_rooms_subq, booked_rooms_subq.c.rooms_id == Rooms.id)
                .group_by(Hotels.id, Rooms.id, booked_rooms_subq.c.booked_count)
                .having((Rooms.quantity - func.coalesce(booked_rooms_subq.c.booked_count, 0)) > 0)
            )

            result = await session.execute(query)
            return result.scalars().unique().all()
class RoomDAO(BaseDAO):
    model = Rooms
    @classmethod
    async def find_available_by_hotel_and_dates(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # Подсчет уже забронированных номеров
            booked_rooms = (
                select(
                    Bookings.rooms_id,
                    func.count().label("booked")
                )
                .where(
                    and_(
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                )
                .group_by(Bookings.rooms_id)
                .cte("booked_rooms")
            )

            # Основной запрос по номерам
            query = (
                select(
                    Rooms,
                    (Rooms.price * func.DATE_PART("day", date_to - date_from)).label("total_cost"),
                    (Rooms.quantity - func.coalesce(booked_rooms.c.booked, 0)).label("rooms_left")
                )
                .outerjoin(booked_rooms, booked_rooms.c.rooms_id == Rooms.id)
                .where(Rooms.hotel_id == hotel_id)
            )

            result = await session.execute(query)
            return result.all()
        
        @classmethod
        async def find_by_id(cls, hotel_id: int):
            async with async_session_maker() as session:
                query = select(Hotels).where(Hotels.id == hotel_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            
        