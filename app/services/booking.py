from datetime import datetime, timedelta

from fastapi import HTTPException
from starlette import status

from app.models import User, Booking, MeetingRoom
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreateSchema
from app.services.meeting_room import MeetingRoomService


class BookingService:
    def __init__(self, booking_repository: BookingRepository, meeting_room_service: MeetingRoomService):
        self.booking_repository = booking_repository
        self.meeting_room_service = meeting_room_service

    async def get_all(self) -> list[Booking]:
        return await self.booking_repository.get_all()

    async def get_by_id(self, booking_id: int) -> Booking | None:
        return await self.booking_repository.get_by_id(booking_id)

    async def create(self, booking_data: BookingCreateSchema, current_user: User) -> Booking:
        meeting_room = await self.meeting_room_service.get_by_id(booking_data.meeting_room_id)
        if not meeting_room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        if not await self.__check_booking_conflict(booking_data, meeting_room, None):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is booked for this time"
            )
        new_booking = await self.booking_repository.create(booking_data, current_user)
        return new_booking

    async def delete(self, booking_id: int, current_user: User) -> bool:
        booking = await self.booking_repository.get_by_id(booking_id)

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
        await self.booking_repository.delete(booking)
        return True

    async def update(self, booking_id: int, booking_data: BookingCreateSchema, current_user: User) -> Booking:

        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        meeting_room = await self.meeting_room_service.get_by_id(booking_data.meeting_room_id)
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

        if not await self.__check_booking_conflict(booking_data, meeting_room, booking_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is booked for this time"
            )
        updated_booking = await self.booking_repository.update(booking, booking_data)
        return updated_booking

    async def __check_booking_conflict(
            self,
            booking_data: BookingCreateSchema,
            meeting_room: MeetingRoom,
            exclude_booking_id: int | None = None
    ) -> bool:
        start_dt = datetime.combine(booking_data.date, booking_data.meeting_starts_at)
        end_dt = start_dt + timedelta(
            hours=booking_data.meeting_duration.hour,
            minutes=booking_data.meeting_duration.minute,
            seconds=booking_data.meeting_duration.second
        )
        bookings_at_date_in_room = await self.booking_repository.get_by_meeting_room_id_and_booking_date(
            meeting_room_id=meeting_room.id,
            booking_date=booking_data.date,
            exclude_booking_id=exclude_booking_id
        )

        for booking in bookings_at_date_in_room:
            booking_start = datetime.combine(booking.date, booking.meeting_starts_at)
            booking_duration = timedelta(
                hours=booking.meeting_duration.hour,
                minutes=booking.meeting_duration.minute,
                seconds=booking.meeting_duration.second
            )
            booking_end = booking_start + booking_duration
            if start_dt < booking_end and end_dt > booking_start:
                return False
        return True