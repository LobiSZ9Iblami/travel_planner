from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends

from app.db.database import get_session
from app.repositories.travel_place_repository import TravelPlaceRepository
from app.repositories.travel_project_repository import TravelProjectRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.travel_project = TravelProjectRepository(self.session)
        self.place = TravelPlaceRepository(self.session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()


async def get_uow(session: AsyncSession = Depends(get_session)):
    async with UnitOfWork(session) as uow:
        yield uow
