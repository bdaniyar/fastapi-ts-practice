from datetime import time
import time
from fastapi.middleware import Middleware
import redis.asyncio as redis
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import sentry_sdk
from sqladmin import Admin, ModelView
from starlette.middleware.sessions import SessionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

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
from fastapi_tasks_db.databasework.logger import logger
from fastapi_versioning import VersionedFastAPI, version
from fastapi_tasks_db.databasework.prometheus.router import router as prometheus_router

app = FastAPI()

sentry_sdk.init(
    dsn="https://8d7af38c5556b32134292a6caf3bc336@o4509701250809856.ingest.de.sentry.io/4509701256380496",
    send_default_pii=True,
)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(hotels_router)
app.include_router(images_router)
app.include_router(prometheus_router)
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

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    #description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)

admin.add_view(BookingsAdmin)

admin.add_view(HotelsAdmin)

admin.add_view(RoomsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process time": round(process_time,4)
    })
    return response

app.mount(
    "/static",
    StaticFiles(directory="fastapi_tasks_db/databasework/static"),
    name="static",
)