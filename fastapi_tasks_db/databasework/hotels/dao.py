from datetime import date

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import joinedload

from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.dao.base import BaseDAO
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.hotels.models import Hotels, Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_available_by_location_and_dates(
        cls, location: str, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            bookings_for_selected_dates = (
                select(Bookings)
                .where(
                    or_(
                        and_(
                            Bookings.date_from < date_to, Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to,
                        ),
                    )
                )
                .subquery("filtered_bookings")
            )
            hotels_rooms_left = (
                select(
                    *Hotels.__table__.columns,
                    Rooms.hotel_id.label("hotel_id"),  # 🔥 ЭТО ОБЯЗАТЕЛЬНО
                    (
                        Hotels.rooms_quantity
                        - func.count(bookings_for_selected_dates.c.rooms_id)
                    ).label("rooms_left"),
                )
                .select_from(Hotels)
                .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(
                    bookings_for_selected_dates,
                    bookings_for_selected_dates.c.rooms_id == Rooms.id,
                )
                .where(Hotels.location.contains(location.title()))
                .group_by(Hotels.id, Rooms.hotel_id)
                .cte("hotels_rooms_left")
            )

            get_hotels_info = (
                select(
                    *Hotels.__table__.columns,
                    hotels_rooms_left.c.rooms_left,
                )
                .select_from(Hotels)
                .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
                .where(hotels_rooms_left.c.rooms_left > 0)
            )

            result = await session.execute(get_hotels_info)
            return result.all()


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_available_by_hotel_and_dates(
        cls, hotel_id: int, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            # Подсчет уже забронированных номеров
            booked_rooms = (
                select(Bookings.rooms_id, func.count().label("booked"))
                .where(and_(Bookings.date_from < date_to, Bookings.date_to > date_from))
                .group_by(Bookings.rooms_id)
                .cte("booked_rooms")
            )

            # Основной запрос по номерам
            query = (
                select(
                    Rooms,
                    (Rooms.price * func.DATE_PART("day", date_to - date_from)).label(
                        "total_cost"
                    ),
                    (Rooms.quantity - func.coalesce(booked_rooms.c.booked, 0)).label(
                        "rooms_left"
                    ),
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
