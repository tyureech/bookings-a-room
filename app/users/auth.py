from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password + settings.SALT)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + settings.SALT, hashed_password)


async def auth_login(email: str, password: str):
    existing_user = await UserDAO.get_one_or_none(email=email)
    if (
        existing_user
        and email == existing_user.email
        and verify_password(password, existing_user.hashed_password)
    ):
        return existing_user
    raise IncorrectEmailOrPasswordException


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
