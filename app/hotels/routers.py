from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.main import cache

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(ttl="1m", prefix="fastapi_cache")
async def get_hotels(location: str, date_from: date, date_to: date):
    return await HotelDAO.find_hotels_with_rooms_left(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    return await HotelDAO.get_one_or_none(id=hotel_id)
