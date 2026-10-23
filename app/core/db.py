from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import get_db_url


SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        return session