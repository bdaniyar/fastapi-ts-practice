from fastapi_tasks_db.databasework.database import async_session_maker
from sqlalchemy import select

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls,model_id:int):
        if cls.model is None:
            raise ValueError("Model is not defined in DAO subclass")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_more(cls, **filter_by):
        if cls.model is None:
            raise ValueError("Model is not defined in DAO subclass")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by):
        if cls.model is None:
            raise ValueError("Model is not defined in DAO subclass")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()