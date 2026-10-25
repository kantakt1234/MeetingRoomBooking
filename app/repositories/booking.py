from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Booking


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

    async def create(self, user_id: int, meeting_room_id: int,
                     start_at: datetime, end_at: datetime) -> Booking:
        booking = Booking(
            user_id=user_id,
            meeting_room_id=meeting_room_id,
            start_at=start_at,
            end_at=end_at,
        )

        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def delete(self, booking: Booking) -> bool:
        await self.session.delete(booking)
        await self.session.commit()
        return True

    async def update(self, booking: Booking, meeting_room_id: int,
                     start_at: datetime, end_at: datetime) -> Booking:
        booking.meeting_room_id = meeting_room_id
        booking.start_at = start_at
        booking.end_at = end_at
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def get_overlapping(self, start_at: datetime, end_at: datetime) -> list[Booking]:
        query = select(Booking).where(Booking.start_at < end_at, Booking.end_at > start_at)
        result = await self.session.execute(query)
        return list(result.scalars().all())
