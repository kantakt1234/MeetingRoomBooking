from app.core.exceptions import RoomIsNotFoundError
from app.repositories.meeting_room import MeetingRoomRepository
from app.schemas.meeting_room import MeetingRoomResponseSchema, MeetingRoomUpdateSchema, MeetingRoomCreateSchema


class MeetingRoomService:
    def __init__(self, meeting_room_repository: MeetingRoomRepository):
        self.meeting_room_repository = meeting_room_repository

    async def get_all(self) -> list[MeetingRoomResponseSchema]:
        meeting_rooms = await self.meeting_room_repository.get_all()
        meeting_rooms = [MeetingRoomResponseSchema.model_validate(meeting_room) for meeting_room in meeting_rooms]
        return meeting_rooms

    async def get_by_id(self, meeting_room_id: int) -> MeetingRoomResponseSchema:
        meeting_room = await self.meeting_room_repository.get_by_id(meeting_room_id)
        if not meeting_room:
            raise RoomIsNotFoundError()
        return MeetingRoomResponseSchema.model_validate(meeting_room)

    async def create(self, meeting_room_data: MeetingRoomCreateSchema) -> MeetingRoomResponseSchema:
        meeting_room = await self.meeting_room_repository.create(meeting_room_data.description)
        return MeetingRoomResponseSchema.model_validate(meeting_room)

    async def delete(self, meeting_room_id: int) -> bool:
        meeting_room = await self.meeting_room_repository.get_by_id(meeting_room_id)
        if not meeting_room:
            raise RoomIsNotFoundError()
        await self.meeting_room_repository.delete(meeting_room)
        return True

    async def update(self, meeting_room_id: int, meeting_room_data: MeetingRoomUpdateSchema) -> MeetingRoomResponseSchema:
        meeting_room = await self.meeting_room_repository.get_by_id(meeting_room_id)
        if not meeting_room:
            raise RoomIsNotFoundError()
        result = await self.meeting_room_repository.update(meeting_room, meeting_room_data.description)
        return MeetingRoomResponseSchema.model_validate(result)