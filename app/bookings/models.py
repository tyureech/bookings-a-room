from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class Booking(Base):
    
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))

    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")

    def __str__(self) -> str:
        return f'booking #{self.id}'