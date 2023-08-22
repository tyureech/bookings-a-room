from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email, password_1, password_2, code", [
        ("test@test.ru", "test", "test", 200),
        ("test@test.ru", "test2", "test2", 409),
        ("test2@test.ru", "test1", "test2", 409),

    ]
)
async def test_register_user(email: str, password_1: str, password_2: str, code: int, ac: AsyncClient):
    response = await ac.post("/users/register", json={
            "email": email, 
            "password1": password_1, 
            "password2": password_2
        }
    )
    
    assert response.status_code == code

@pytest.mark.parametrize("email, password, code, is_token", [
        ("wrong@user.com", "qwerty", 401, False),
        ('tyureech@yandex.ru', 'string', 200, True),
        ('tyureech@yandex.ru', 'password', 401, False)
    ]
)
async def test_login_user(email, password, code, is_token, ac: AsyncClient):
    response = await ac.post("/users/login", json={
            "email": email,
            "password": password,
        }
    )
    assert (response.cookies.get('access_token') is not None) == is_token
    assert response.status_code == code

async def test_logout_user(authenticated_ac: AsyncClient):
    assert authenticated_ac.cookies.get('access_token')
    responce = await authenticated_ac.post("/users/logout")
    assert not authenticated_ac.cookies.get('access_token')
    assert not responce.cookies.get('access_token')