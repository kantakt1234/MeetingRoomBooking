from pydantic import BaseModel


class BaseMeetingRoomSchema(BaseModel):
    description: str


class GetBaseMeetingRoomSchema(BaseMeetingRoomSchema):
    id: int