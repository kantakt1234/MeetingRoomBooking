import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class BookingCreateSchema(BaseModel):
    meeting_room_id: int
    start_at: datetime.datetime
    end_at: datetime.datetime

    @model_validator(mode="after")
    def check_dates(self) -> Self:
        for value in (self.start_at, self.end_at):
            if value.tzinfo is None:
                raise ValueError("time must include a timezone offset")
            if value.second or value.microsecond:
                raise ValueError("time must be in whole minutes")
        if self.end_at <= self.start_at:
            raise ValueError("end_at must be later than start_at")
        if self.start_at < datetime.datetime.now(datetime.timezone.utc):
            raise ValueError("start_at must be in the future")
        return self


class BookingUpdateSchema(BookingCreateSchema):
    pass


class BookingSchema(BookingCreateSchema):
    id: int
    user_id: int


class BookingResponseSchema(BookingSchema):
    model_config = ConfigDict(from_attributes=True)


class BookingDeleteResponseSchema(BaseModel):
    result: bool
