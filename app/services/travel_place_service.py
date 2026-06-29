from datetime import UTC, datetime

from app.uow.uow import UnitOfWork
from app.external_api.art_institute import ArtInstituteClient
from app.core.exceptions import (
    AlreadyExistsException,
    BadRequestException,
    NotFoundException
)
from app.models.travel_place import TravelPlace
from app.schemas.travel_place_schema import (
    TravelPlaceCreate,
    TravelPlaceListResponse,
    TravelPlaceResponse,
    TravelPlaceUpdate
)


class TravelPlaceService:

    def __init__(self, uow: UnitOfWork, art_institute:ArtInstituteClient):
        self.uow = uow
        self.art_institute = art_institute

    async def add_place(
        self,
        project_id: int,
        data: TravelPlaceCreate,
    ) -> TravelPlaceResponse:

        project = await self.uow.travel_project.get_by_id(project_id)

        if project is None:
            raise NotFoundException(
                detail="Travel project not found."
            )

        places = await self.uow.place.list_by_project(project_id)

        if len(places) >= 10:
            raise BadRequestException(
                detail="Travel project cannot contain more than 10 places."
            )

        existing_place = await self.uow.place.get_by_external_id(
            project_id,
            data.external_place_id,
        )

        if existing_place:
            raise AlreadyExistsException(
                detail="Place already exists in project."
            )

        await self.art_institute.get_artwork_or_raise(
            data.external_place_id
        )

        place = TravelPlace(
            travel_project_id=project_id,
            external_place_id=data.external_place_id,
            title=data.title,
            notes=data.notes,
        )

        await self.uow.place.add(place)
        await self.uow.session.flush()

        return TravelPlaceResponse.model_validate(place)

    async def update_place(
        self,
        place_id: int,
        data: TravelPlaceUpdate,
    ) -> TravelPlaceResponse:

        place = await self.uow.place.get_by_id(place_id)

        if place is None:
            raise NotFoundException(
                detail="Travel place not found."
            )

        if data.notes is not None:
            place.notes = data.notes

        if data.visited is not None:
            place.visited = data.visited

            place.visited_at = (
                datetime.now(UTC)
                if data.visited
                else None
            )

        await self.uow.session.flush()
        place = await self.uow.place.get_by_id(place_id)

        return TravelPlaceResponse.model_validate(place)

    async def get_place(
        self,
        project_id: int,
        external_id: str
    ) -> TravelPlaceResponse:

        place = await self.uow.place.get_by_external_id(project_id, external_id)

        if place is None:
            raise NotFoundException(
                detail="Travel place not found."
            )

        return TravelPlaceResponse.model_validate(place)

    async def list_places(
        self,
        project_id: int,
    ) -> TravelPlaceListResponse:

        places = await self.uow.place.list_by_project(project_id)

        return TravelPlaceListResponse(
            items=[
                TravelPlaceResponse.model_validate(place)
                for place in places
            ]
        )
