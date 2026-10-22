import datetime

from sqlalchemy import ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    meeting_room_id: Mapped[int] = mapped_column(ForeignKey("meeting_rooms.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    meeting_starts_at: Mapped[datetime.time] = mapped_column(Time)
    meeting_duration: Mapped[datetime.time] = mapped_column(Time)

