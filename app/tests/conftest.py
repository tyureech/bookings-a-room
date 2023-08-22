import asyncio
import pytest
from sqlalchemy import insert
from httpx import AsyncClient

from app.main import app
from app.config import settings
from app.users.models import User
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.bookings.models import Booking
from app.tests.models import TestModel
from app.database import Base, engine, async_session_maker

from app.tests.moc_data import MOC_DATA_USERS, MOC_DATA_HOTELS,\
    MOC_DATA_ROOMS, MOC_DATA_BOKINGS, MOC_DATA_TEST_MODEL


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        add_users = insert(User).values(MOC_DATA_USERS)
        add_hotels = insert(Hotel).values(MOC_DATA_HOTELS)
        add_rooms = insert(Room).values(MOC_DATA_ROOMS)
        add_booking = insert(Booking).values(MOC_DATA_BOKINGS)
        add_test_models = insert(TestModel).values(MOC_DATA_TEST_MODEL)
        
        await session.execute(add_users)
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_booking)
        await session.execute(add_test_models)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac 

@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/users/login", json={
            "email": "tyureech@yandex.ru",
            "password": "string"
        })
        yield ac
