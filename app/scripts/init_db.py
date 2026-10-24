import asyncio

from app.core.auth import get_password_hash
from app.core.config import settings
from app.core.db import engine, async_session
from app.models import User
from app.repositories.user import UserRepository


async def init_db() -> None:
    async with async_session() as session:
        user = await UserRepository(session).get_by_login(settings.SUPERUSER_LOGIN)
        if not user:
            password = get_password_hash(settings.SUPERUSER_PASSWORD)
            new_user = User()
            new_user.name = settings.SUPERUSER_NAME
            new_user.is_admin = True
            new_user.login = settings.SUPERUSER_LOGIN
            new_user.password_hash = password
            session.add(new_user)
            await session.commit()
    await engine.dispose()


if __name__ == "__main__":
    print("Инициализация базы данных...")
    asyncio.run(init_db())
    print("Готово!")