from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.db import get_session
from app.models import User, MeetingRoom
from app.models.booking import Booking
from app.schemas.booking import BookingCreateSchema

booking_router = APIRouter(prefix='/booking', tags=['Booking'])


@booking_router.get('')
def get_bookings(session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)):
    bookings = session.query(Booking).all()
    return bookings


@booking_router.get('/{booking_id}')
def get_booking(booking_id: int, session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
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
    start_dt = datetime.combine(booking_data.date, booking_data.meeting_starts_at)
    end_dt = start_dt + timedelta(
        hours=booking_data.meeting_duration.hour,
        minutes=booking_data.meeting_duration.minute,
        seconds=booking_data.meeting_duration.second
    )
    existing_bookings = session.query(Booking).where(
        Booking.meeting_room_id == meeting_room.id,
        Booking.date == booking_data.date
    ).all()

    for existing in existing_bookings:
        existing_start = datetime.combine(existing.date, existing.meeting_starts_at)
        existing_duration = timedelta(
            hours=existing.meeting_duration.hour,
            minutes=existing.meeting_duration.minute,
            seconds=existing.meeting_duration.second
        )
        existing_end = existing_start + existing_duration
        if start_dt < existing_end and end_dt > existing_start:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is booked for this time"
            )
    session.add(booking)
    session.commit()
    return {'result': 'success'}


@booking_router.delete('/{booking_id}')
def delete_booking(booking_id: int, session: Session = Depends(get_session),
                   current_user: User = Depends(get_current_user)):
    booking = session.query(Booking).where(Booking.id == booking_id).one_or_none()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
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
    if current_user.id != booking.user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    start_dt = datetime.combine(booking_data.date, booking_data.meeting_starts_at)
    end_dt = start_dt + timedelta(
        hours=booking_data.meeting_duration.hour,
        minutes=booking_data.meeting_duration.minute,
        seconds=booking_data.meeting_duration.second
    )
    existing_bookings = session.query(Booking).where(
        Booking.meeting_room_id == meeting_room.id,
        Booking.date == booking_data.date,
        Booking.id != booking_id
    ).all()

    for existing in existing_bookings:
        existing_start = datetime.combine(existing.date, existing.meeting_starts_at)
        existing_duration = timedelta(
            hours=existing.meeting_duration.hour,
            minutes=existing.meeting_duration.minute,
            seconds=existing.meeting_duration.second
        )
        existing_end = existing_start + existing_duration
        if start_dt < existing_end and end_dt > existing_start:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is booked for this time"
            )
    booking.meeting_room_id = booking_data.meeting_room_id
    booking.meeting_duration = booking_data.meeting_duration
    booking.date = booking_data.date
    booking.meeting_starts_at = booking_data.meeting_starts_at
    session.commit()
    return {"result": "success"}