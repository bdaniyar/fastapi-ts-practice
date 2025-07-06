from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel
from datetime import date
from typing import List
class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int

class SRoomInfo(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int

    class Config:
        from_attributes = True

class SBookingInfo(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str
    services: List[str]

    class Config:
        from_attributes = True