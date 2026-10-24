from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_auth_data
from app.core.db import get_session
from app.core.exceptions import InvalidTokenError, TokenIsExpiredError, InvalidTokenPayloadError, UserIsNotFoundError, \
    NotEnoughRightsError, TokenNotFoundError
from app.repositories.booking import BookingRepository
from app.repositories.meeting_room import MeetingRoomRepository
from app.repositories.user import UserRepository
from app.schemas.user import CurrentUserSchema
from app.services.booking import BookingService
from app.services.meeting_room import MeetingRoomService
from app.services.user import UserService


def get_booking_service(session: AsyncSession = Depends(get_session)) -> BookingService:
    booking_repository = BookingRepository(session)
    meeting_room_service = get_meeting_room_service(session)
    booking_service = BookingService(booking_repository, meeting_room_service)
    return booking_service


def get_meeting_room_service(session: AsyncSession = Depends(get_session)) -> MeetingRoomService:
    meeting_room_repository = MeetingRoomRepository(session)
    meeting_room_service = MeetingRoomService(meeting_room_repository)
    return meeting_room_service


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    return user_service


def get_token(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFoundError()
    return token


async def get_current_user(
        token: str = Depends(get_token),
        session: AsyncSession = Depends(get_session)
) -> CurrentUserSchema:

    try:
        auth_data = get_auth_data()

        payload = jwt.decode(
            token,
            auth_data["secret_key"],
            algorithms=[auth_data['algorithm']],
            options={"require_exp": True}
        )

    except ExpiredSignatureError:
        raise TokenIsExpiredError()
    except JWTError:
        raise InvalidTokenError()

    try:
        user_id = int(payload.get('sub'))
    except (TypeError, ValueError):
        raise InvalidTokenPayloadError()

    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(int(user_id))

    if not user:
        raise UserIsNotFoundError()

    user = CurrentUserSchema.model_validate(user)

    return user


def get_current_admin_user(
        current_user: CurrentUserSchema = Depends(get_current_user)
) -> CurrentUserSchema:

    if current_user.is_admin:
        return current_user
    raise NotEnoughRightsError()