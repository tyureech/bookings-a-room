import sentry_sdk
from cashews import cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_versioning import VersionedFastAPI
from sqladmin import Admin

from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.routers import router as router_booking
from app.config import settings
from app.database import engine
from app.hotels.rooms.routers import router as router_rooms
from app.hotels.routers import router as router_hotel
from app.images.routers import router as router_images
from app.pages.routers import router as router_pages
from app.users.routers import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(router_booking)
app.include_router(router_hotel)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


cache.setup("redis://localhost")


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
)


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)


app.mount("/app/static", StaticFiles(directory="app/static"), name="static")


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)
