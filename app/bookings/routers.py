from datetime import date
from fastapi import APIRouter, Depends, status
from app.bookings.dao import BookingDAO
from app.exceptions import RoomFullyBooked
from app.tasks.tasks import send_mail
from app.users.dependencies import get_current_user
from app.bookings.schemas import SBookings
from app.users.models import User


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/user")
async def get_user_bookings(user: User = Depends(get_current_user)):
    bookings = await BookingDAO.get_all_bookings_info(user_id=user.id)
    return bookings


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_bookings(
    room_id: int,
    date_from: date,
    date_to: date,
    price: int | None,
    user: User = Depends(get_current_user),
):
    bookings = await BookingDAO.add(room_id, date_from, date_to, price, user.id)
    if bookings:
        send_mail.delay(
            to_emails=[user.email],
            subject="Бронирование номера",
            message=f"<h1>Вы забронировали номер с {bookings.date_from} до {bookings.date_to}.<h1>",
        )
        return bookings
    raise RoomFullyBooked


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)):
    return await BookingDAO.get_all_bookings_info()


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delte_booking(booking_id: int, user: User = Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id)
