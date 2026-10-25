from app.core.exceptions import RoomIsNotFoundError, RoomIsBookedError, BookingIsNotFoundError, ForbiddenError
from app.models import User, Booking
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreateSchema, BookingResponseSchema
from app.services.meeting_room import MeetingRoomService


class BookingService:
    def __init__(self, booking_repository: BookingRepository, meeting_room_service: MeetingRoomService):
        self.booking_repository = booking_repository
        self.meeting_room_service = meeting_room_service

    async def get_all(self) -> list[BookingResponseSchema]:
        bookings = await self.booking_repository.get_all()
        bookings = [BookingResponseSchema.model_validate(booking) for booking in bookings]
        return bookings

    async def get_by_id(self, booking_id: int) -> BookingResponseSchema:
        booking = await self._get_booking_or_raise(booking_id)
        return BookingResponseSchema.model_validate(booking) if booking else None

    async def create(self, booking_data: BookingCreateSchema, current_user: User) -> BookingResponseSchema:
        meeting_room = await self.meeting_room_service.get_by_id(booking_data.meeting_room_id)
        if not meeting_room:
            raise RoomIsNotFoundError()

        if await self.booking_repository.get_overlapping(booking_data.start_at, booking_data.end_at):
            raise RoomIsBookedError()

        new_booking = await self.booking_repository.create(
            current_user.id, booking_data.meeting_room_id,
            booking_data.start_at, booking_data.end_at,
        )

        return BookingResponseSchema.model_validate(new_booking)

    async def delete(self, booking_id: int, current_user: User) -> bool:
        booking = await self._get_booking_or_raise(booking_id)

        if booking.user_id != current_user.id and not current_user.is_admin:
            raise ForbiddenError()

        await self.booking_repository.delete(booking)
        return True

    async def update(self, booking_id: int, booking_data: BookingCreateSchema, current_user: User) -> BookingResponseSchema:
        booking = await self._get_booking_or_raise(booking_id)

        meeting_room = await self.meeting_room_service.get_by_id(booking_data.meeting_room_id)
        if not meeting_room:
            raise RoomIsNotFoundError()

        if current_user.id != booking.user_id and not current_user.is_admin:
            raise ForbiddenError()

        if await self.booking_repository.get_overlapping(booking_data.start_at, booking_data.end_at):
            raise RoomIsBookedError()

        updated_booking = await self.booking_repository.update(
            booking,
            meeting_room.id,
            booking_data.start_at,
            booking_data.end_at,
        )
        return BookingResponseSchema.model_validate(updated_booking)

    async def _get_booking_or_raise(self, booking_id: int) -> Booking:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise BookingIsNotFoundError()
        return booking