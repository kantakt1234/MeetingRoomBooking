from fastapi import HTTPException, status

from app.core.auth import get_password_hash, verify_password, create_access_token
from app.models import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegisterSchema, UserLoginSchema


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, user_data: UserRegisterSchema) -> User:
        if self.get_by_login(user_data.login):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this login already exists"
            )
        user = await self.user_repository.create(user_data)
        return user


    async def get_by_login(self, login: str) -> User | None:
        return await self.user_repository.get_by_login(login)

    async def auth(self, user_data: UserLoginSchema) -> str:
        user = await self.user_repository.get_by_login(user_data.login)
        if not user or verify_password(plain_password=user_data.password,
                                       hashed_password=str(user.password_hash)) == False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password"
            )
        access_token = create_access_token({"sub": str(user.id)})
        return access_token