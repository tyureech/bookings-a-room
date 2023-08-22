from sqlalchemy import select, func
from app.database import async_session_maker, engine
from app.dao.base import BaseDAO
from app.bookings.models import Booking
from app.hotels.rooms.models import Room


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def find_all(cls, hotel_id, date_from, date_to):
        """
        WITH booked_rooms AS (
            SELECT bookings.room_id FROM bookings
                WHERE (bookings.date_from >= '2012-12-12' AND bookings.date_from < '2012-12-13'
                OR bookings.date_from <= '2012-12-12' AND bookings.date_to > '2012-12-12')
        ),
        rooms_left AS(
                SELECT rooms.id as room_id, rooms.quantity - count(booked_rooms.room_id) AS left
                FROM rooms LEFT OUTER JOIN booked_rooms ON rooms.id = booked_rooms.room_id
                GROUP BY rooms.id, rooms.quantity
        )
        SELECT rooms.*, rooms_left.left, (rooms.price * ('2012-12-19'::date - '2012-12-12'::date)) AS total_coast
        FROM rooms
        LEFT JOIN rooms_left
        ON rooms.id = rooms_left.room_id
        WHERE rooms.hotel_id = 1
        """
        async with async_session_maker() as session:
            subquery_booked_rooms = (
                select(Booking.room_id)
                .where(
                    ((Booking.date_from >= date_from) & (Booking.date_from < date_to))
                    | ((Booking.date_from <= date_from) & (Booking.date_to > date_from))
                )
                .cte("booked_rooms")
            )

            subquery_rooms_left = (
                select(
                    Room.id.label("room_id"),
                    (Room.quantity - func.count(subquery_booked_rooms.c.room_id)).label(
                        "left"
                    ),
                )
                .join(
                    subquery_booked_rooms,
                    Room.id == subquery_booked_rooms.c.room_id,
                    isouter=True,
                )
                .group_by(Room.id, Room.quantity)
                .cte("rooms_left")
            )

            rooms_in_hotel = (
                select(
                    Room.__table__.columns,
                    subquery_rooms_left.c.left,
                    (Room.price * (date_to - date_from).days).label("total_coast"),
                )
                .join(subquery_rooms_left, Room.id == subquery_rooms_left.c.room_id)
                .where(Room.hotel_id == hotel_id)
            )

            print(
                rooms_in_hotel.compile(engine, compile_kwargs={"literal_binds": True})
            )

            booked_rooms = await session.execute(rooms_in_hotel)
            return booked_rooms.mappings().all()
