from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi_tasks_db.databasework.bookings.router import router as router_bookings
from fastapi_tasks_db.databasework.users.router import router as router_users
from fastapi_tasks_db.databasework.pages.router import router as router_pages
from fastapi_tasks_db.databasework.hotels.router import router as hotels_router
from fastapi_tasks_db.databasework.images.router import router as images_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="fastapi_tasks_db/databasework/static"), name="static")
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
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Authorization"]
)