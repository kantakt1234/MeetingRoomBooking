from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash
from app.models import User
from app.schemas.user import UserRegisterSchema


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_login(self, login: str) -> User | None:
        query = select(User).where(User.login == login)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    def create(self, user_data: UserRegisterSchema):
        password = get_password_hash(user_data.password)
        user = User()
        user.name = user_data.name
        user.is_admin = False
        user.login = user_data.login
        user.password_hash = password
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user