from fastapi import FastAPI, status, Request
from starlette.responses import JSONResponse

from app.routers.booking import booking_router
from app.routers.meeting_room import meeting_room_router
from app.routers.user import user_router
from app.core.exceptions import (RoomIsNotFoundError, RoomIsBookedError,
                                 BookingIsNotFoundError, ForbiddenError,
                                 InvalidCredentialsError, LoginIsAlreadyTakenError,
                                 UserIsNotFoundError, InvalidTokenError,
                                 TokenIsExpiredError, InvalidTokenPayloadError,
                                 NotEnoughRightsError, TokenNotFoundError)


app = FastAPI()

app.include_router(meeting_room_router)
app.include_router(user_router)
app.include_router(booking_router)


@app.get("/")
async def root():
    return {"message": "Meeting Room Booking Api", "version": "1.0.0"}


@app.exception_handler(RoomIsNotFoundError)
def room_is_not_found_error_handler(request: Request, exc: RoomIsNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Room is not found"},
    )


@app.exception_handler(RoomIsBookedError)
def room_is_booked_error_handler(request: Request, exc: RoomIsBookedError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Room is already booked on this time"},
    )


@app.exception_handler(BookingIsNotFoundError)
def booking_is_not_found_error_handler(request: Request, exc: BookingIsNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Booking is not found"},
    )


@app.exception_handler(ForbiddenError)
def forbidden_error_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Forbidden"},
    )


@app.exception_handler(InvalidCredentialsError)
def invalid_credentials_error_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials"},
    )


@app.exception_handler(LoginIsAlreadyTakenError)
def login_is_already_taken_error_handler(request: Request, exc: LoginIsAlreadyTakenError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Login is already taken"},
    )


@app.exception_handler(UserIsNotFoundError)
def user_is_not_found_error_handler(request: Request, exc: UserIsNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User is not found"},
    )


@app.exception_handler(InvalidTokenError)
def invalid_token_error_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token"},
    )


@app.exception_handler(TokenIsExpiredError)
def token_is_expired_error_handler(request: Request, exc: TokenIsExpiredError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Token is expired"},
    )


@app.exception_handler(InvalidTokenPayloadError)
def invalid_token_payload_error_handler(request: Request, exc: InvalidTokenPayloadError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token payload"},
    )


@app.exception_handler(NotEnoughRightsError)
def not_enough_rights_error_handler(request: Request, exc: NotEnoughRightsError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Not enough rights"},
    )


@app.exception_handler(TokenNotFoundError)
def token_not_found_error_handler(request: Request, exc: TokenNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Token not found"},
    )