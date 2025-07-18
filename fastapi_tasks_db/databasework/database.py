from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from fastapi_tasks_db.databasework.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL_ASYNC
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL_ASYNC
    DATABASE_PARAMS = {}
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


"""
Файл database.py мы создавали для настройки подключения к базе данных и создания базового класса моделей. Он нужен, чтобы централизованно управлять соединением с БД в проекте на SQLAlchemy + FastAPI.

Вот зачем каждая часть:

⸻

🔹 create_async_engine(settings.DATABASE_URL_ASYNC)

Создаёт асинхронный движок SQLAlchemy, чтобы работать с базой (например, PostgreSQL) через asyncpg.

⸻

🔹 async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Создаёт фабрику сессий (сеансов), которые позволяют делать запросы к базе:
	•	expire_on_commit=False — означает, что объекты не будут становиться «устаревшими» после коммита и ты сможешь сразу их использовать.

⸻

🔹 class Base(DeclarativeBase): pass

Создаёт базовый класс моделей, от которого будут наследоваться все ORM-модели, например:
class Users(Base):
    __tablename__ = "users"
    ...

    Это нужно, чтобы потом Alembic или SQLAlchemy могли управлять схемой таблиц.

⸻

💡 Зачем вообще нужен database.py?

Чтобы всё связанное с базой было в одном месте:
	•	подключение (движок)
	•	фабрика сессий
	•	базовый ORM-класс

Это улучшает читаемость и позволяет переиспользовать это во всём проекте.
"""
