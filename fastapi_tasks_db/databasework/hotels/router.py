from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_tasks_db.databasework.bookings.dao import BookingDAO
from fastapi_tasks_db.databasework.hotels.dao import HotelDAO, RoomDAO
from fastapi_tasks_db.databasework.hotels.schemas import SBookingInfo, SHotel, SRoomInfo
from datetime import date

from fastapi_tasks_db.databasework.users.dependencies import get_current_user
from fastapi_tasks_db.databasework.users.users import Users

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/{location}", response_model=list[SHotel])
async def get_hotels(
    location: str,
    date_from: date = Query(..., alias="date_from"),
    date_to: date = Query(..., alias="date_to")
):
    # Здесь вызываем HotelDAO и фильтруем по location и датам (псевдокод)
    hotels = await HotelDAO.find_available_by_location_and_dates(location, date_from, date_to)
    return hotels


@router.get("/{hotel_id}/rooms", response_model=list[SRoomInfo])
async def get_rooms(
    hotel_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...)
):
    rooms = await RoomDAO.find_available_by_hotel_and_dates(hotel_id, date_from, date_to)

    # Результат приходит как список tuples — [(Room, total_cost, rooms_left)]
    return [
        SRoomInfo(
            **room.__dict__,
            total_cost=total_cost,
            rooms_left=rooms_left
        ) for room, total_cost, rooms_left in rooms
    ]

@router.get("/id/{hotel_id}", response_model=SHotel)
async def get_hotel_by_id(hotel_id: int):
    hotel = await HotelDAO.find_by_id(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel