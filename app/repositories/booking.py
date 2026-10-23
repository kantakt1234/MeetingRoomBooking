from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Booking, User
from app.schemas.booking import BookingCreateSchema


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Booking]:
        query = select(Booking)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, booking_id: int) -> Booking | None:
        query = select(Booking).where(Booking.id == booking_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, booking_data: BookingCreateSchema, current_user: User) -> Booking:
        booking = Booking(
            user_id=current_user.id,
            meeting_room_id=booking_data.meeting_room_id,
            date=booking_data.date,
            meeting_starts_at=booking_data.meeting_starts_at,
            meeting_duration=booking_data.meeting_duration
        )

        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def delete(self, booking: Booking) -> bool:
        await self.session.delete(booking)
        await self.session.commit()
        return True

    async def update(self, booking: Booking, booking_data: BookingCreateSchema) -> Booking:
        booking.meeting_room_id = booking_data.meeting_room_id
        booking.meeting_duration = booking_data.meeting_duration
        booking.date = booking_data.date
        booking.meeting_starts_at = booking_data.meeting_starts_at
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def get_by_meeting_room_id_and_booking_date(
            self,
            meeting_room_id: int,
            booking_date: date,
            exclude_booking_id: int | None = None
    ) -> list[Booking]:
        query = select(Booking).where(
            Booking.meeting_room_id == meeting_room_id,
            Booking.date == booking_date,
        )
        if exclude_booking_id:
            query = query.where(Booking.id != exclude_booking_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
