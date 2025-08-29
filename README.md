# Hotel Booking API (FastAPI)

This project is a Hotel Booking API built with FastAPI. It provides endpoints for user authentication, hotel and room search, room booking, image processing, background tasks, monitoring, and admin management.

## Key Features
- User registration, login (JWT via HttpOnly cookie), logout, and profile (/auth/me)
- Search available hotels by location and dates
- List rooms in a hotel with availability, total cost, and remaining quantity
- Create and view bookings, delete bookings
- Versioned API endpoints (fastapi-versioning)
- Caching layer for heavy hotel search (Redis + fastapi-cache2)
- Background tasks: email confirmations & image processing (Celery + Redis)
- Admin panel (sqladmin) for managing Users, Bookings, Hotels, Rooms
- Static files & image resizing pipeline
- Structured JSON logging
- Metrics & monitoring (Prometheus + Grafana + /metrics endpoint)
- Error handling with custom HTTP exceptions
- Sentry integration for error tracking

## Tech Stack
- Python 3.11, FastAPI, Starlette
- PostgreSQL (asyncpg + SQLAlchemy 2.0 ORM)
- Alembic (database migrations)
- Redis (cache + Celery broker)
- Celery & Flower (task queue & monitoring)
- Prometheus & Grafana (metrics & dashboards)
- JWT (python-jose / PyJWT) for auth tokens
- Pydantic v2 for validation
- Docker & docker-compose for local orchestration

## Environment Variables (.env example)
```
MODE=DEV
LOG_LEVEL=INFO
DB_HOST=localhost
DB_PORT=5432
DB_NAME=booking
DB_USER=postgres
DB_PASS=postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_NAME=booking_test
TEST_DB_USER=postgres
TEST_DB_PASS=postgres
SMTP_USER=your_email@example.com
SMTP_PASS=your_email_password
SMTP_HOST=smtp.example.com
SMTP_PORT=465
REDIS_HOST=redis
REDIS_PORT=6379
```

## Installation (Local without Docker)
1. Create virtual environment
   python3.11 -m venv .venv
   source .venv/bin/activate
2. Install dependencies
   pip install -r requirements.txt
3. Start PostgreSQL & Redis locally
4. Apply migrations
   alembic upgrade head
5. Run app
   uvicorn fastapi_tasks_db.databasework.main:app --reload

Visit: http://localhost:8000/docs

## Docker Setup
Build and start full stack:
```
docker compose up --build
```
Services:
- booking_app: FastAPI (port 7777 -> 8000 internal)
- booking_db: PostgreSQL (port 5432)
- booking_redis: Redis
- booking_celery: Celery worker
- booking_flower: Flower UI (http://localhost:5555)
- prometheus: http://localhost:9090
- grafana: http://localhost:3000 (add Prometheus datasource: http://prometheus:9090)

App base URL (versioned): http://localhost:7777/v1 or /v2 for versioned endpoints.

## Authentication Flow
1. User registers with email & password (hashed via bcrypt)
2. Login returns JWT (30 min expiry) stored as HttpOnly cookie booking_access_token
3. Protected routes use dependency get_current_user (decode & validate token)
4. Logout clears cookie.

## Background Tasks
- Celery task process_pic resizes images into 1000x500 and 200x100.
- Booking confirmation email (send_booking_confirmation_email) dispatched via BackgroundTasks or Celery.

## Logging
Structured JSON logs with timestamp, level, message. LOG_LEVEL configurable.

## Monitoring
- prometheus_fastapi_instrumentator exposes default FastAPI metrics.
- Use Grafana dashboard (grafana-dashboard.json) to visualize.

## Testing
Pytest setup with async support (pytest-asyncio). Separate TEST_* database config. To run tests:
```
pytest -q
```

## Migrations
Generate new migration:
```
alembic revision --autogenerate -m "desc"
```
Apply migrations:
```
alembic upgrade head
```

## Make a Booking (Example)
1. Register & login
2. GET /hotels/{location}?date_from=2025-09-01&date_to=2025-09-05
3. GET /hotels/{hotel_id}/rooms?date_from=2025-09-01&date_to=2025-09-05
4. POST /bookings rooms_id=1&date_from=2025-09-01&date_to=2025-09-05
5. GET /bookings to see your booking

## Error Handling
Custom exceptions in exceptions.py provide meaningful HTTP status & messages.

## Security Notes
- JWT stored in HttpOnly cookie to mitigate XSS token theft
- Use HTTPS in production & set cookie secure flag
- Rotate SECRET_KEY on compromise.

