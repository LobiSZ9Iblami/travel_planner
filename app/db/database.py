from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings


postgres_url = settings.db.postgresql_url


engine = create_async_engine(postgres_url, echo=True)


async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
