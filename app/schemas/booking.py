import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class BookingCreateSchema(BaseModel):
    meeting_room_id: int
    start_at: datetime.datetime
    end_at: datetime.datetime

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end_at < self.start_at:
            raise ValueError("start_at must be before end_at")
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
