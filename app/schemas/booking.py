import datetime

from pydantic import BaseModel, ConfigDict


class BookingCreateSchema(BaseModel):
    meeting_room_id: int
    date: datetime.date
    meeting_starts_at: datetime.time
    meeting_duration: datetime.time


class BookingSchema(BookingCreateSchema):
    id: int
    user_id: int


class BookingResponseSchema(BookingSchema):
    model_config = ConfigDict(from_attributes=True)


class BookingDeleteResponseSchema(BaseModel):
    result: bool
