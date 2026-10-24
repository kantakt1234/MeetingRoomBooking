from app.core.auth import verify_password, create_access_token, get_password_hash
from app.core.exceptions import LoginIsAlreadyTakenError, InvalidCredentialsError, UserIsNotFoundError
from app.repositories.user import UserRepository
from app.schemas.user import UserRegisterSchema, UserResponseSchema, UserCredentialsSchema


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, user_data: UserRegisterSchema) -> UserResponseSchema:
        if await self.user_repository.get_by_login(user_data.login):
            raise LoginIsAlreadyTakenError()
        password = get_password_hash(user_data.password)
        user = await self.user_repository.create(password, user_data)
        return UserResponseSchema.model_validate(user)


    async def get_by_login(self, login: str) -> UserResponseSchema:
        user = await self.user_repository.get_by_login(login)
        if not user:
            raise UserIsNotFoundError()
        return UserResponseSchema.model_validate(user)

    async def auth(self, user_data: UserCredentialsSchema) -> str:
        user = await self.user_repository.get_by_login(user_data.login)
        if not user or verify_password(plain_password=user_data.password,
                                       hashed_password=str(user.password_hash)) == False:
            raise InvalidCredentialsError()
        access_token = create_access_token({"sub": str(user.id)})
        return access_token
