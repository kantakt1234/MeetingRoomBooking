from fastapi import HTTPException, status

from app.repositories.meeting_room import MeetingRoomRepository
from app.schemas.meeting_room import BaseMeetingRoomSchema


class MeetingRoomService:
    def __init__(self, meeting_room_repository: MeetingRoomRepository):
        self.meeting_room_repository = meeting_room_repository

    async def get_all(self):
        return await self.meeting_room_repository.get_all()

    async def get_by_id(self, meeting_room_id: int):
        meeting_room = await self.meeting_room_repository.get_by_id(meeting_room_id)
        return meeting_room

    async def create(self, meeting_room_data: BaseMeetingRoomSchema):
        return await self.meeting_room_repository.create(meeting_room_data)

    async def delete(self, meeting_room_id: int):
        meeting_room = await self.get_by_id(meeting_room_id)
        if not meeting_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        await self.meeting_room_repository.delete(meeting_room)
        return True

    async def update(self, meeting_room_id: int, meeting_room_data: BaseMeetingRoomSchema):
        meeting_room = await self.get_by_id(meeting_room_id)
        if not meeting_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        result = await self.meeting_room_repository.update(meeting_room, meeting_room_data)
        return result