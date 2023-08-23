from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (IncorrectTokenFormatException,
                            TokenDoesNotExistException, TokenExpiredException,
                            UserIsNotPresentException)
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenDoesNotExistException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire = payload.get("exp")
    if not expire or datetime.utcnow().timestamp() > int(expire):
        raise TokenExpiredException
    user_id = payload.get("id")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.get_by_id(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
