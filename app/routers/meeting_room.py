from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_current_admin_user
from app.core.db import get_session
from app.models import MeetingRoom, User
from app.repositories.meeting_room import MeetingRoomRepository
from app.schemas.meeting_room import BaseMeetingRoomSchema
from app.services.meeting_room import MeetingRoomService

meeting_room_router = APIRouter(prefix='/meeting_room', tags=["Meeting room"])


def get_meeting_room_service(session: AsyncSession = Depends(get_session)) -> MeetingRoomService:
    meeting_room_repository = MeetingRoomRepository(session)
    meeting_room_service = MeetingRoomService(meeting_room_repository)
    return meeting_room_service

@meeting_room_router.get('')
async def get_meeting_rooms(meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
                    current_user: User = Depends(get_current_user)):
    meeting_rooms = await meeting_room_service.get_all()
    return meeting_rooms


@meeting_room_router.get('/{room_id}')
async def get_meeting_room(meeting_room_id: int, meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
                   current_user: User = Depends(get_current_user)):
    meeting_room = await meeting_room_service.get_by_id(meeting_room_id)
    if meeting_room:
        return meeting_room
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found"
    )

@meeting_room_router.post('/')
async def create_meeting_room(meeting_room_data: BaseMeetingRoomSchema, meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
                      current_user: User = Depends(get_current_admin_user)):
    meeting_room = await meeting_room_service.create(meeting_room_data)
    return meeting_room


@meeting_room_router.delete('/{room_id}')
async def delete_meeting_room(meeting_room_id: int, meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
                      current_user: User = Depends(get_current_admin_user)):
    result = await meeting_room_service.delete(meeting_room_id)
    return result


@meeting_room_router.put('/{room_id}')
async def put_meeting_room(room_id: int, room: BaseMeetingRoomSchema, meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
                   current_user: User = Depends(get_current_admin_user)):
    await meeting_room_service.update(room_id, room)
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == room_id).one_or_none()
    if meeting_room:
        meeting_room.description = room.description
        session.commit()
        return {"result": "success"}
    raise HTTPException(status_code=404, detail='Not found')
