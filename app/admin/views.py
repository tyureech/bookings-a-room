from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.booking]
    can_delete = False
    can_edit = False
    name_plural = "Пользователи"
    page_size = 20
    icon = "fa-solid fa-user"


class HotelAdmin(ModelView, model=Hotel):
    column_exclude_list = [Hotel.room]
    form_excluded_columns = [Hotel.room]
    name_plural = "Отели"
    page_size = 20
    can_delete = False
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_exclude_list = [Room.booking, Room.hotel_id]
    form_excluded_columns = [Room.booking]
    name_plural = "Комнаты"
    page_size = 20
    can_delete = False
    icon = "fa-solid fa-door-open"


class BookingAdmin(ModelView, model=Booking):
    column_exclude_list = [Booking.room_id, Booking.user_id]
    form_excluded_columns = [Booking.total_cost, Booking.total_days]
    name_plural = "Брони"
    page_size = 20
    icon = "fa-solid fa-book-open"
