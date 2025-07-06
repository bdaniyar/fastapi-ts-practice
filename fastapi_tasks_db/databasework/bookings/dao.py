from datetime import date
from sqlalchemy import select, delete, insert, func, and_ , or_
from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.dao.base import BaseDAO
from fastapi_tasks_db.databasework.database import async_session_maker
from fastapi_tasks_db.databasework.hotels.models import Rooms
from fastapi_tasks_db.databasework.database import engine 


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        rooms_id: int,
        date_from: date,
        date_to: date,
        ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR 
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
            SELECT rooms. quantity - COUNT(booked_rooms. room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms. room_id = rooms. id
            WHERE rooms. id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
             booked_rooms = select(Bookings).where(
            and_(
                Bookings.rooms_id == rooms_id,
                or_(
                    and_(
                        Bookings.date_from >= date_from, 
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from, 
                        Bookings.date_to > date_from
                    )
                )
            )
        ).cte("booked_rooms")


        get_rooms_left = select(
            (Rooms.quantity - func.count(booked_rooms.c.rooms_id)).label("rooms_left")
            ).select_from(Rooms).join (
                booked_rooms, booked_rooms.c.rooms_id == Rooms.id , isouter=True
            ).where(Rooms.id == rooms_id).group_by(
                Rooms.quantity, booked_rooms.c.rooms_id
            )
        print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
        
        #rooms_left = await session.execute(get_rooms_left) 
        #rooms_left : int = rooms_left.scalar()
        rooms_left_result = await session.execute(get_rooms_left)
        rooms_left = rooms_left_result.scalar()

        if not rooms_left or rooms_left <= 0:
            return None
        if rooms_left > 0:
            get_price = select(Rooms.price).filter_by(id=rooms_id)
            price = await session.execute(get_price)
            price = price.scalar()
            add_booking = insert(Bookings).values(
                rooms_id=rooms_id, 
                user_id=user_id,
                date_from=date_from, 
                date_to=date_to, 
                price=price,
            ).returning(Bookings)

            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()
        else:
            return None
        
    @classmethod
    async def find_all_by_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Bookings, Rooms)
                .join(Rooms, Bookings.rooms_id == Rooms.id)
                .where(Bookings.user_id == user_id)
                .order_by(Bookings.date_from)
            )
            result = await session.execute(query)
            return result.all()
        
    @classmethod
    async def delete_by_id(cls, booking_id: int) -> bool:
        async with async_session_maker() as session:
            query = delete(Bookings).where(Bookings.id == booking_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def get_bookings_with_room_info(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.price,
                    (Bookings.date_to - Bookings.date_from).label("total_days"),
                    ((Bookings.date_to - Bookings.date_from) * Rooms.price).label("total_cost"),
                )
                .join(Rooms, Rooms.id == Bookings.rooms_id)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.all()
