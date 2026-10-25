import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    meeting_room_id: Mapped[int] = mapped_column(ForeignKey("meeting_rooms.id"))

    start_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
