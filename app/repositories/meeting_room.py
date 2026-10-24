from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MeetingRoom


class MeetingRoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[MeetingRoom]:
        query = select(MeetingRoom)
        meeting_rooms = await self.session.execute(query)
        return list(meeting_rooms.scalars().all())

    async def get_by_id(self, meeting_room_id: int) -> MeetingRoom | None:
        query = select(MeetingRoom).where(MeetingRoom.id == meeting_room_id)
        meeting_room = await self.session.execute(query)
        return meeting_room.scalars().one_or_none()

    async def create(self, description: str) -> MeetingRoom:
        meeting_room = MeetingRoom(description=description)
        self.session.add(meeting_room)
        await self.session.commit()
        await self.session.refresh(meeting_room)
        return meeting_room

    async def delete(self, meeting_room: MeetingRoom) -> bool:
        await self.session.delete(meeting_room)
        await self.session.commit()
        return True

    async def update(self, meeting_room: MeetingRoom, description: str) -> MeetingRoom:
        meeting_room.description = description
        await self.session.commit()
        await self.session.refresh(meeting_room)
        return meeting_room