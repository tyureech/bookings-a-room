from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import DateFromCannotBeAfterDateTo, RoomFullyBooked, RoomNotFound
from app.hotels.rooms.models import Room


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add(cls, new_booking, user_id):
        """
        WITH booked_rooms AS(
            SELECT room_id from bookings
            WHERE room_id = 1 AND (
                    ('2023-06-10'::date <= date_from and '2023-06-30'::date > date_from)
                OR
                    ('2023-06-10'::date >= date_from and '2023-06-10' < date_to)
            )
        )
        SELECT rooms.quantity - count(booked_rooms.room_id) from rooms
        LEFT JOIN booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        GROUP BY quantity
        """
        if new_booking.date_from >= new_booking.date_to:
            raise DateFromCannotBeAfterDateTo

        async with async_session_maker() as session:
            subquery_booked_rooms = (
                select(cls.model.room_id)
                .where(
                    and_(
                        or_(
                            and_(
                                new_booking.date_from <= cls.model.date_from,
                                new_booking.date_to > cls.model.date_from,
                            ),
                            and_(
                                new_booking.date_from >= cls.model.date_from,
                                new_booking.date_from < cls.model.date_to,
                            ),
                        ),
                        new_booking.room_id == cls.model.room_id,
                    ),
                )
                .cte("booked_rooms")
            )

            query_rooms_left = (
                select(Room.quantity - func.count(subquery_booked_rooms.c.room_id))
                .join_from(Room, subquery_booked_rooms, isouter=True)
                .where(Room.id == new_booking.room_id)
                .group_by(Room.quantity)
            )

            rooms_left = await session.execute(query_rooms_left)
            count_rooms_left: int = rooms_left.scalar()
            if count_rooms_left is None:
                raise RoomNotFound
            if count_rooms_left <= 0:
                raise RoomFullyBooked

            query_price = select(Room.price).where(Room.id == new_booking.room_id)
            price = await session.execute(query_price)
            price: int = price.scalar()
            add_new_bookings = (
                insert(cls.model)
                .values(
                    room_id=new_booking.room_id,
                    date_from=new_booking.date_from,
                    date_to=new_booking.date_to,
                    price=new_booking.price,
                    user_id=user_id,
                )
                .returning(cls.model)
            )
            booking = await session.execute(add_new_bookings)
            await session.commit()
            return booking.scalar()

    @classmethod
    async def get_all_bookings_info(cls, user_id: int = None):
        async with async_session_maker() as session:
            query_bookings = (
                select(
                    cls.model.room_id,
                    cls.model.user_id,
                    cls.model.date_from,
                    cls.model.date_to,
                    cls.model.price,
                    cls.model.total_cost,
                    cls.model.total_days,
                    Room.image_id,
                    Room.name,
                    Room.description,
                    Room.services,
                )
                .join_from(cls.model, Room, isouter=True)
                .where(user_id is None or cls.model.user_id == user_id)
            )
            # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            bookings = await session.execute(query_bookings)
            return bookings.mappings().all()
