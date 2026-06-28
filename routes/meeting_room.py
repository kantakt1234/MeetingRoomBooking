from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_session
from models import MeetingRoom
from schemas.meeting_room import BaseMeetingRoomSchema


meeting_room_router = APIRouter(prefix='/meeting_room')


@meeting_room_router.get('')
def get_rooms(session: Session = Depends(get_session)):
    meeting_rooms = session.query(MeetingRoom).all()
    return meeting_rooms


@meeting_room_router.get('/{room_id}')
def get_room(room_id: int, session: Session = Depends(get_session)):
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == room_id).one()
    if meeting_room:
        return meeting_room
    else:
        raise HTTPException(status_code=404, detail='Not found')

@meeting_room_router.post('/')
def create_room(room: BaseMeetingRoomSchema, session: Session = Depends(get_session)):
    meeting_room = MeetingRoom(description=room.description)
    session.add(meeting_room)
    session.commit()
    return {"result": "success"}


@meeting_room_router.delete('/{room_id}')
def delete_room(room_id: int, session: Session = Depends(get_session)):
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == room_id).one()
    if meeting_room:
        session.delete(meeting_room)
        session.commit()
        return {"result": "success"}
    else:
        raise HTTPException(status_code=404, detail='Not found')

@meeting_room_router.put('/{room_id}')
def put_room(room_id: int, room: BaseMeetingRoomSchema, session: Session = Depends(get_session)):
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == room_id).one()
    if meeting_room:
        meeting_room.description = room.description
        session.commit()
    else:
        raise HTTPException(status_code=404, detail='Not found')
