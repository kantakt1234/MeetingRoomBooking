from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.models.booking import Booking


class MeetingRoom(Base):
    __tablename__ =  "meeting_rooms"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)

    bookings: Mapped[list['Booking']] = relationship()