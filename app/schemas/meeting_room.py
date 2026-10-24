from pydantic import BaseModel, ConfigDict


class MeetingRoomCreateSchema(BaseModel):
    description: str


class MeetingRoomUpdateSchema(MeetingRoomCreateSchema):
    pass


class MeetingRoomSchema(MeetingRoomCreateSchema):
    id: int


class MeetingRoomResponseSchema(MeetingRoomSchema):
    model_config = ConfigDict(from_attributes=True)


class MeetingRoomDeleteResponseSchema(BaseModel):
    result: bool