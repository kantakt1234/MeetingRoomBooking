class RoomIsNotFoundError(Exception):
    pass


class RoomIsBookedError(Exception):
    pass


class BookingIsNotFoundError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class LoginIsAlreadyTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserIsNotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class TokenIsExpiredError(Exception):
    pass


class InvalidTokenPayloadError(Exception):
    pass


class NotEnoughRightsError(Exception):
    pass


class TokenNotFoundError(Exception):
    pass