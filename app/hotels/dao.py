
from sqlalchemy import select, text, func, and_, or_
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.database import async_session_maker, engine


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def find_hotels_with_rooms_left(cls, location, date_to, date_from):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings 
            WHERE ('2012-12-12' <= bookings.date_from AND '2012-12-13' > bookings.date_from
            OR '2012-12-12' >= bookings.date_from AND '2012-12-12' < bookings.date_to) 
        ),
        rooms_left AS(
            SELECT rooms.hotel_id as hotel_id, rooms.quantity - count(booked_rooms.room_id) AS left 
            FROM rooms LEFT OUTER JOIN booked_rooms ON rooms.id = booked_rooms.room_id 
            GROUP BY rooms.hotel_id, rooms.quantity
        )

        SELECT hotels.*, sum(rooms_left.left)
        FROM hotels
        LEFT JOIN rooms_left
        ON hotels.id = rooms_left.hotel_id
        WHERE hotels.location LIKE '%Алтай%'
        GROUP BY hotels.id
        ORDER BY hotels.name
        """
        async with async_session_maker() as session:
            subquery_booked_rooms = select(Booking.room_id.label('room_id'))\
            .where(
                or_(
                    and_(date_from <= Booking.date_from, date_to > Booking.date_from),
                    and_(date_from >= Booking.date_from, date_to < Booking.date_to)
                )
            ).cte("booked_rooms")

            subquery_count_rooms_left = select(
                    Room.hotel_id.label('hotel_id'),
                    (Room.quantity - func.count(subquery_booked_rooms.c.room_id)).label("count_left")
                ).join(
                    subquery_booked_rooms, 
                    Room.id == subquery_booked_rooms.c.room_id,
                    isouter=True
                ).group_by(
                    Room.hotel_id, 
                    Room.quantity
                ).cte('count_rooms_left')
            
            query_left_rooms = select(
                    Hotel.__table__.columns, 
                    func.sum(subquery_count_rooms_left.c.count_left).label('count_left_rooms')
                ).join(
                    subquery_count_rooms_left,
                    Hotel.id == subquery_count_rooms_left.c.hotel_id,
                    isouter=True
                ).where(
                    Hotel.location.like(f"%{location}%") 
                ).group_by(
                    Hotel.id,
                )
            
            left_rooms = await session.execute(query_left_rooms)
            
            # print(query_left_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            return left_rooms.mappings().all()
