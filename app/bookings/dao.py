from sqlalchemy import insert, select, and_, or_, func

from app.database import async_session_maker, engine
from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.exceptions import DateFromCannotBeAfterDateTo
from app.hotels.rooms.models import Room


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add(cls, room_id, date_from, date_to, price, user_id):
        """
        WITH booked_rooms AS(
            SELECT * from bookings
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
        if date_from >= date_to:
            raise DateFromCannotBeAfterDateTo

        async with async_session_maker() as session:
            query_booked_rooms = (
                select(cls.model)
                .where(
                    and_(
                        or_(
                            and_(
                                date_from <= cls.model.date_from,
                                date_to > cls.model.date_from,
                            ),
                            and_(
                                date_from >= cls.model.date_from,
                                date_from < cls.model.date_to,
                            ),
                        ),
                        room_id == cls.model.room_id,
                    ),
                )
                .cte("booked_rooms")
            )

            query_free_rooms = (
                select(Room.quantity - func.count(query_booked_rooms.c.room_id))
                .join_from(Room, query_booked_rooms, isouter=True)
                .where(Room.id == room_id)
                .group_by(Room.quantity)
            )

            # print(query_free_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            free_rooms = await session.execute(query_free_rooms)
            count_free_rooms: int = free_rooms.scalar()
            if count_free_rooms > 0:
                query_price = select(Room.price).where(Room.id == room_id)
                price = await session.execute(query_price)
                price: int = price.scalar()
                add_bookings = (
                    insert(cls.model)
                    .values(
                        room_id=room_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                        user_id=user_id,
                    )
                    .returning(cls.model)
                )
                bookings = await session.execute(add_bookings)
                await session.commit()
                return bookings.scalar()

    @classmethod
    async def get_all_bookings_info(cls, user_id: int = None):
        async with async_session_maker() as session:
            query = (
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
            bookings = await session.execute(query)
            return bookings.mappings().all()
