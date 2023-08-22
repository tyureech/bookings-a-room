from pydantic import BaseModel, EmailStr

class SRegister(BaseModel):
    email: EmailStr
    password1: str
    password2: str

class SLogin(BaseModel):
    email: EmailStr
    password: str
