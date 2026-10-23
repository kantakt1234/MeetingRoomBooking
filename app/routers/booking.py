from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.models import User
from app.repositories.booking import BookingRepository
from app.routers.meeting_room import get_meeting_room_service
from app.schemas.booking import BookingCreateSchema
from app.services.booking import BookingService

booking_router = APIRouter(prefix='/booking', tags=['Booking'])


def get_booking_service(session: AsyncSession = Depends(get_session)) -> BookingService:
    booking_repository = BookingRepository(session)
    meeting_room_service = get_meeting_room_service(session)
    booking_service = BookingService(booking_repository, meeting_room_service)
    return booking_service


@booking_router.get('')
async def get_bookings(booking_service: BookingService = Depends(get_booking_service),
                       current_user: User = Depends(get_current_user)):
    bookings = await booking_service.get_all()
    return bookings


@booking_router.get('/{booking_id}')
async def get_booking(booking_id: int, booking_service: BookingService = Depends(get_booking_service),
                      current_user: User = Depends(get_current_user)):
    booking = await booking_service.get_by_id(booking_id)
    if booking:
        return booking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found"
    )


@booking_router.post('/')
async def create_booking(booking_data: BookingCreateSchema, booking_service: BookingService = Depends(get_booking_service),
                         current_user: User = Depends(get_current_user)):
    booking = await booking_service.create(booking_data, current_user)
    return booking


@booking_router.delete('/{booking_id}')
async def delete_booking(booking_id: int, booking_service: BookingService = Depends(get_booking_service),
                         current_user: User = Depends(get_current_user)):
    result = booking_service.delete(booking_id, current_user)
    return {"result": result}


@booking_router.put('/{booking_id}')
async def put_booking(booking_id: int, booking_data: BookingCreateSchema, booking_service: BookingService = Depends(get_booking_service),
                      current_user: User = Depends(get_current_user)):
    result = await booking_service.update(booking_id, booking_data, current_user)
    return result