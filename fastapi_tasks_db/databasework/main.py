import redis.asyncio as redis
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from sqladmin import Admin, ModelView
from starlette.middleware.sessions import SessionMiddleware

from fastapi_tasks_db.databasework.admin.auth import authentication_backend
from fastapi_tasks_db.databasework.admin.views import (BookingsAdmin,
                                                       HotelsAdmin, RoomsAdmin,
                                                       UsersAdmin)
from fastapi_tasks_db.databasework.bookings.router import \
    router as router_bookings
from fastapi_tasks_db.databasework.config import settings
from fastapi_tasks_db.databasework.database import engine
from fastapi_tasks_db.databasework.hotels.router import router as hotels_router
from fastapi_tasks_db.databasework.images.router import router as images_router
from fastapi_tasks_db.databasework.pages.router import router as router_pages
from fastapi_tasks_db.databasework.users.router import router as router_users

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="fastapi_tasks_db/databasework/static"),
    name="static",
)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(hotels_router)
app.include_router(images_router)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Authorization",
    ],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.on_event("startup")
async def startup():
    r = redis.Redis(host=f"{settings.REDIS_HOST}", port=settings.REDIS_PORT, db=0)
    FastAPICache.init(RedisBackend(r), prefix="cache")


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)

admin.add_view(BookingsAdmin)

admin.add_view(HotelsAdmin)

admin.add_view(RoomsAdmin)
