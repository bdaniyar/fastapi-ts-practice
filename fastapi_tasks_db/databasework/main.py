from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel

from fastapi_tasks_db.databasework.bookings.router import router as router_bookings
from fastapi_tasks_db.databasework.users.router import router as router_users
app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


class SHotel(BaseModel):
    address: str
    name: str
    stars: int

@app.get("/hotels")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Optional[bool] = None,
    stars: Optional[int] = Query(None, ge=1,le=5)
):
    return date_from, date_to
class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date



@app.post("/bookings")
def add_booking(booking:SBooking):
    pass