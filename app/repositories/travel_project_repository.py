from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TravelProject


class TravelProjectRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, project: TravelProject) -> TravelProject:
        self.session.add(project)
        return project

    async def get_by_id(self, project_id: int) -> TravelProject | None:
        result = await self.session.execute(
            select(TravelProject).where(TravelProject.id == project_id)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[TravelProject]:
        result = await self.session.execute(
            select(TravelProject)
        )
        return result.scalars().all()

    async def delete(self, project: TravelProject) -> None:
        await self.session.delete(project)
