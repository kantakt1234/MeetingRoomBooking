from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserRegisterSchema


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, password: str, user_data: UserRegisterSchema) -> User:
        user = User()
        user.name = user_data.name
        user.is_admin = False
        user.login = user_data.login
        user.password_hash = password
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()