from fastapi import APIRouter, Depends

from app.dependencies import get_booking_service, get_current_user
from app.models import User
from app.schemas.booking import BookingCreateSchema, BookingResponseSchema, BookingDeleteResponseSchema, \
    BookingUpdateSchema
from app.services.booking import BookingService

booking_router = APIRouter(prefix='/booking', tags=['Booking'])


@booking_router.get('')
async def get_bookings(
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user)
) -> list[BookingResponseSchema]:

    return await booking_service.get_all()


@booking_router.get('/{booking_id}')
async def get_booking(
        booking_id: int,
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user)
) -> BookingResponseSchema:

    return await booking_service.get_by_id(booking_id)


@booking_router.post('/')
async def create_booking(
        booking_data: BookingCreateSchema,
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user)
) -> BookingResponseSchema:

    return await booking_service.create(booking_data, current_user)


@booking_router.delete('/{booking_id}')
async def delete_booking(
        booking_id: int,
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user)
) -> BookingDeleteResponseSchema:

    result = await booking_service.delete(booking_id, current_user)
    return BookingDeleteResponseSchema(result=result)


@booking_router.put('/{booking_id}')
async def update_booking(
        booking_id: int,
        booking_data: BookingUpdateSchema,
        booking_service: BookingService = Depends(get_booking_service),
        current_user: User = Depends(get_current_user)
) -> BookingResponseSchema:

    return await booking_service.update(booking_id, booking_data, current_user)