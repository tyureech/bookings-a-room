from datetime import date

from pydantic import BaseModel


class SBookings(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    price: int
