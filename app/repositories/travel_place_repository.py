from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.travel_place import TravelPlace


class TravelPlaceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, place: TravelPlace) -> TravelPlace:
        self.session.add(place)
        return place

    async def get_by_id(self, place_id: int) -> TravelPlace | None:
        result = await self.session.execute(
            select(TravelPlace).where(TravelPlace.id == place_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: int) -> list[TravelPlace]:
        result = await self.session.execute(
            select(TravelPlace)
            .where(TravelPlace.travel_project_id == project_id)
            .order_by(TravelPlace.id)
        )
        return result.scalars().all()

    async def get_by_external_id(
        self,
        project_id: int,
        external_id: str
    ) -> TravelPlace | None:

        result = await self.session.execute(
            select(TravelPlace).where(
                TravelPlace.travel_project_id == project_id,
                TravelPlace.external_place_id == external_id
            )
        )
        return result.scalar_one_or_none()
