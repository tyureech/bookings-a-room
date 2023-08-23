from sqlalchemy import and_, func, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def find_hotels_with_rooms_left(cls, location, date_from, date_to):
        """
        WITH booked_rooms AS (
            SELECT room_id
            FROM bookings
            WHERE
                '2012-12-12' <= bookings.date_from AND '2012-12-13' > bookings.date_from
                OR '2012-12-12' >= bookings.date_from AND '2012-12-12' < bookings.date_to
        ),
        rooms_left AS(
            SELECT
                rooms.hotel_id as hotel_id,
                rooms.quantity - count(booked_rooms.room_id) AS rooms
            FROM rooms
            LEFT OUTER JOIN booked_rooms
            ON rooms.id = booked_rooms.room_id
            GROUP BY rooms.hotel_id, rooms.quantity
        )

        SELECT hotels.*, sum(rooms_left.rooms)
        FROM hotels
        LEFT JOIN rooms_left
        ON hotels.id = rooms_left.hotel_id
        WHERE hotels.location LIKE '%Алтай%'
        GROUP BY hotels.id
        ORDER BY hotels.name
        """
        async with async_session_maker() as session:
            subquery_booked_rooms = (
                select(Booking.room_id.label("room_id"))
                .where(
                    or_(
                        and_(date_from <= Booking.date_from, date_to > Booking.date_from),
                        and_(date_from >= Booking.date_from, date_from < Booking.date_to),
                    )
                )
                .cte("booked_rooms")
            )

            subquery_rooms = (
                select(
                    Room.hotel_id.label("hotel_id"),
                    (Room.quantity - func.count(subquery_booked_rooms.c.room_id)).label(
                        "rooms_left"
                    ),
                )
                .join(
                    subquery_booked_rooms,
                    Room.id == subquery_booked_rooms.c.room_id,
                    isouter=True,
                )
                .group_by(Room.hotel_id, Room.quantity)
                .cte("rooms_left")
            )

            query_hotels = (
                select(
                    Hotel.__table__.columns,
                    func.sum(subquery_rooms.c.rooms_left).label(
                        "rooms_left"
                    ),
                )
                .join(
                    subquery_rooms,
                    Hotel.id == subquery_rooms.c.hotel_id,
                    isouter=True,
                )
                .where(Hotel.location.like(f"%{location}%"))
                .group_by(
                    Hotel.id,
                )
            )

            hotels = await session.execute(query_hotels)
            return hotels.mappings().all()
