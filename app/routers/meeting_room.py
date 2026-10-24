from fastapi import APIRouter, Depends

from app.dependencies import get_meeting_room_service, get_current_user, get_current_admin_user
from app.models import User
from app.schemas.meeting_room import MeetingRoomCreateSchema, MeetingRoomResponseSchema, MeetingRoomUpdateSchema, \
    MeetingRoomDeleteResponseSchema
from app.services.meeting_room import MeetingRoomService

meeting_room_router = APIRouter(prefix='/meeting_room', tags=["Meeting room"])


@meeting_room_router.get('')
async def get_meeting_rooms(
        meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
        current_user: User = Depends(get_current_user)
) -> list[MeetingRoomResponseSchema]:

    return await meeting_room_service.get_all()


@meeting_room_router.get('/{meeting_room_id}')
async def get_meeting_room(
        meeting_room_id: int,
        meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
        current_user: User = Depends(get_current_user)
) -> MeetingRoomResponseSchema:

    return await meeting_room_service.get_by_id(meeting_room_id)


@meeting_room_router.post('/')
async def create_meeting_room(
        meeting_room_data: MeetingRoomCreateSchema,
        meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
        current_user: User = Depends(get_current_admin_user)
) -> MeetingRoomResponseSchema:

    return await meeting_room_service.create(meeting_room_data)


@meeting_room_router.delete('/{meeting_room_id}')
async def delete_meeting_room(
        meeting_room_id: int,
        meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
        current_user: User = Depends(get_current_admin_user)
) -> MeetingRoomDeleteResponseSchema:

    result = await meeting_room_service.delete(meeting_room_id)
    return MeetingRoomDeleteResponseSchema(result=result)


@meeting_room_router.put('/{meeting_room_id}')
async def update_meeting_room(
        meeting_room_id: int,
        meeting_room_data: MeetingRoomUpdateSchema,
        meeting_room_service: MeetingRoomService = Depends(get_meeting_room_service),
        current_user: User = Depends(get_current_admin_user)
) -> MeetingRoomResponseSchema:

    return await meeting_room_service.update(meeting_room_id, meeting_room_data)
