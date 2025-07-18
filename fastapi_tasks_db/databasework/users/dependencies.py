from datetime import datetime, timezone

from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from jose import JWTError, jwt

from fastapi_tasks_db.databasework.config import settings
from fastapi_tasks_db.databasework.exceptions import (
    IncorrectTokenFormatException, TokenAbsentException,
    TokenExpiredExceptions, UserIsNotPresentException)
from fastapi_tasks_db.databasework.users.dao import UsersDAO
from fastapi_tasks_db.databasework.users.users import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    except JWTError:
        raise IncorrectTokenFormatException
    expire = payload.get("exp")
    now_ts = int(datetime.now(tz=timezone.utc).timestamp())
    if (not expire) or (int(expire) < now_ts):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    sub = payload.get("sub")
    if sub is None:
        raise TokenExpiredExceptions
    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(user_id)
    if not user:
        raise UserIsNotPresentException

    return user
