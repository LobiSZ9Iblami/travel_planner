from app.uow.uow import UnitOfWork
from app.models.travel_project import TravelProject
from app.models.travel_place import TravelPlace
from app.external_api.art_institute import ArtInstituteClient
from app.schemas.travel_project_schema import (
    TravelProjectCreate,
    TravelProjectUpdate,
    TravelProjectResponse,
    TravelProjectWithPlacesResponse
)
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    AlreadyExistsException
)


class TravelProjectService:

    def __init__(self, uow: UnitOfWork, art_institute:ArtInstituteClient):
        self.uow = uow
        self.art_institute = art_institute

    async def _get_project_with_places(self, project_id: int) -> TravelProject:
        project = await self.uow.travel_project.get_by_id(project_id)

        if not project:
            raise NotFoundException("Project not found")

        # force load places (if lazy)
        await self.uow.session.refresh(project, attribute_names=["places"])

        return project

    async def create_project_with_places(
        self,
        data: TravelProjectCreate
    ) -> TravelProjectWithPlacesResponse:

        if len(data.places) > 10:
            raise BadRequestException("Max 10 places allowed")

        project = TravelProject(
            name=data.name,
            description=data.description,
            start_date=data.start_date
        )

        await self.uow.travel_project.add(project)
        await self.uow.session.flush()

        created_places: list[TravelPlace] = []

        for place in data.places:

            # external validation
            await self.art_institute.get_artwork_or_raise(place.external_place_id)

            # duplicate check
            existing = await self.uow.place.get_by_external_id(
                project.id,
                place.external_place_id
            )

            if existing:
                raise AlreadyExistsException(
                    detail="Place already exists in project"
                )

            travel_place = TravelPlace(
                travel_project_id=project.id,
                external_place_id=place.external_place_id,
                title=place.title,
                notes=place.notes
            )

            await self.uow.place.add(travel_place)
            created_places.append(travel_place)

        await self.uow.session.flush()
        project = await self._get_project_with_places(project.id)

        return TravelProjectWithPlacesResponse.model_validate(project)

    async def delete_project(self, project_id: int) -> None:

        project = await self.uow.travel_project.get_by_id(project_id)

        if not project:
            raise NotFoundException("Project not found")

        places = await self.uow.place.list_by_project(project_id)

        if any(p.visited for p in places):
            raise BadRequestException(
                "Cannot delete project with visited places"
            )

        await self.uow.travel_project.delete(project)
        await self.uow.session.flush()

    async def update_project(
        self,
        project_id: int,
        data: TravelProjectUpdate
    ) -> TravelProjectWithPlacesResponse:

        project = await self.uow.travel_project.get_by_id(project_id)

        if not project:
            raise NotFoundException("Project not found")

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        if data.start_date is not None:
            project.start_date = data.start_date

        await self.uow.session.flush()
        project = await self._get_project_with_places(project_id)

        return TravelProjectWithPlacesResponse.model_validate(project)

    async def get_project(
        self,
        project_id: int
    ) -> TravelProjectWithPlacesResponse:

        project = await self._get_project_with_places(project_id)

        if not project:
            raise NotFoundException("Project not found")

        return TravelProjectWithPlacesResponse.model_validate(project)

    async def list_projects(self) -> list[TravelProjectResponse]:

        projects = await self.uow.travel_project.list()

        return [
            TravelProjectResponse.model_validate(p)
            for p in projects
        ]
