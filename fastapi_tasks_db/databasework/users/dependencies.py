from datetime import datetime, timezone
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, Response, status
from fastapi import Depends, HTTPException, Request

from fastapi_tasks_db.databasework.config import settings
from fastapi_tasks_db.databasework.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload  = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire = payload.get("exp")
    now_ts = int(datetime.now(tz=timezone.utc).timestamp())
    if (not expire) or (int(expire) < now_ts):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UsersDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user