import datetime

from pydantic import BaseModel


class BookingCreateSchema(BaseModel):
    meeting_room_id: int
    date: datetime.date
    meeting_starts_at: datetime.time
    meeting_duration: datetime.time


class BookingSchema(BookingCreateSchema):
    id: int
    user_id: int
