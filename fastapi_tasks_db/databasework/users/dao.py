from fastapi_tasks_db.databasework.dao.base import BaseDAO
from fastapi_tasks_db.databasework.users.users import Users

class UsersDAO(BaseDAO):
    model = Users