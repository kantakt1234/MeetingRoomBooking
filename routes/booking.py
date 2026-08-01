from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.db import get_session
from models import User, MeetingRoom
from models.booking import Booking
from routes.meeting_room import meeting_room_router
from schemas.booking import BookingCreateSchema

booking_router = APIRouter(prefix='/booking', tags=['Booking'])


@booking_router.get('')
def get_bookings(session: Session = Depends(get_session)):
    bookings = session.query(Booking).all()
    return bookings


@booking_router.get('/{booking_id}')
def get_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.query(Booking).where(Booking.id == booking_id).one_or_none()
    if booking:
        return booking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found"
    )


@booking_router.post('/')
def create_booking(booking_data: BookingCreateSchema, session: Session = Depends(get_session),
                   current_user: User = Depends(get_current_user)):
    booking = Booking(
        user_id=current_user.id,
        meeting_room_id=booking_data.meeting_room_id,
        date=booking_data.date,
        meeting_starts_at=booking_data.meeting_starts_at,
        meeting_duration=booking_data.meeting_duration
    )
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == booking_data.meeting_room_id).one_or_none()
    if not meeting_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    session.add(booking)
    session.commit()
    return {'result': 'success'}


@booking_router.delete('/{booking_id}')
def delete_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.query(Booking).where(Booking.id == booking_id).one_or_none()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    session.delete(booking)
    session.commit()
    return {"result": "success"}


@booking_router.put('/{booking_id}')
def put_booking(booking_id: int, booking_data: BookingCreateSchema, session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    booking = session.query(Booking).where(Booking.id == booking_id).one_or_none()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    meeting_room = session.query(MeetingRoom).where(MeetingRoom.id == booking_data.meeting_room_id).one_or_none()
    if not meeting_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    if current_user.id != booking.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    booking.meeting_room_id = booking_data.meeting_room_id
    booking.meeting_duration = booking_data.meeting_duration
    booking.date = booking_data.date
    booking.meeting_starts_at = booking_data.meeting_starts_at
    session.commit()
    return {"result": "success"}