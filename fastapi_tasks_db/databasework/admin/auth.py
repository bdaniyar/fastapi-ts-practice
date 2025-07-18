from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi_tasks_db.databasework.config import settings
from fastapi_tasks_db.databasework.exceptions import \
    IncorrectEmailOrPasswordException
from fastapi_tasks_db.databasework.users.auth import (authenticate_user,
                                                      create_access_token)
from fastapi_tasks_db.databasework.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = str(form["username"]), str(form["password"])
        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await get_current_user(token)
        if user:
            return True
        return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
