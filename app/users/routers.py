from datetime import timedelta

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.exceptions import (
    PasswordsDonNotMatchException,
    UserEmailAlreadyExistsException,
)
from app.users.auth import auth_login, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SLogin, SRegister

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/register")
async def register_user(user: SRegister):
    existing_user = await UserDAO.get_one_or_none(email=user.email)
    if existing_user:
        raise UserEmailAlreadyExistsException
    if user.password1 != user.password2:
        raise PasswordsDonNotMatchException
    hashed_password = get_password_hash(user.password1)
    await UserDAO.add(email=user.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(user_data: SLogin) -> JSONResponse:
    user = await auth_login(user_data.email, user_data.password)
    data = {"id": user["id"]}
    jwt_token = create_access_token(data=data, expires_delta=timedelta(minutes=30))
    responce = JSONResponse({"access_token": jwt_token})
    responce.set_cookie(key="access_token", value=jwt_token, httponly=True)
    return responce


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
