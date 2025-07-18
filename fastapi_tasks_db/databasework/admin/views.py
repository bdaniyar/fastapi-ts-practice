from sqladmin import ModelView

from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.hotels.models import Hotels, Rooms
from fastapi_tasks_db.databasework.users.users import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.rooms,
    ]
    name = "Bookings"
    name_plural = "Bookings"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Hotels"
    name_plural = "Hotels"
    icon = "fa-solid fa-user"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Rooms"
    name_plural = "Rooms"
    icon = "fa-solid fa-user"
