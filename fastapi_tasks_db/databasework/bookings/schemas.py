from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    rooms_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        from_attributes = True


class SBookingInfo(BaseModel):
    id: int
    rooms_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str
    services: list[str]

    class Config:
        from_attributes = True  # заменяет устаревшее orm_mode
