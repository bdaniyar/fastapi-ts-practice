import asyncio
import datetime
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, text

from fastapi_tasks_db.databasework.bookings.m import Bookings
from fastapi_tasks_db.databasework.config import settings
from fastapi_tasks_db.databasework.database import (Base, async_session_maker,
                                                    engine)
from fastapi_tasks_db.databasework.hotels.models import Hotels, Rooms
from fastapi_tasks_db.databasework.main import app as fastapi_app
from fastapi_tasks_db.databasework.users.users import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_detabase():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_json(model: str):
        with open(
            f"fastapi_tasks_db/databasework/tests/{model}.json", encoding="utf-8"
        ) as file:
            return json.load(file)

    hotels = open_json("hotels")
    rooms = open_json("rooms")
    users = open_json("users")
    bookings = open_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")
        # if "total_cost" in booking:
        #     del booking["total_cost"]
        # if "total_days" in booking:
        #     del booking["total_days"]

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "string",
            },
        )
        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
