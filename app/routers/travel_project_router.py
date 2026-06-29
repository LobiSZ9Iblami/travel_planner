from fastapi import APIRouter, Depends, status

from app.schemas.travel_project_schema import (
    TravelProjectCreate,
    TravelProjectUpdate,
    TravelProjectResponse,
    TravelProjectWithPlacesResponse,
)

from app.uow.uow import get_uow, UnitOfWork
from app.services.travel_project_service import TravelProjectService
from app.external_api.art_institute import get_art_institute_client, ArtInstituteClient


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "/",
    response_model=TravelProjectWithPlacesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: TravelProjectCreate,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelProjectWithPlacesResponse:

    service = TravelProjectService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.create_project_with_places(data)


@router.get(
    "/{project_id}",
    response_model=TravelProjectWithPlacesResponse,
)
async def get_project(
    project_id: int,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelProjectWithPlacesResponse:

    service = TravelProjectService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.get_project(project_id)


@router.get(
    "/",
    response_model=list[TravelProjectResponse],
)
async def list_projects(
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> list[TravelProjectResponse]:

    service = TravelProjectService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.list_projects()


@router.patch(
    "/{project_id}",
    response_model=TravelProjectWithPlacesResponse,
)
async def update_project(
    project_id: int,
    data: TravelProjectUpdate,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelProjectWithPlacesResponse:
    service = TravelProjectService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.update_project(
        project_id=project_id,
        data=data,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> None:

    service = TravelProjectService(
        uow=uow,
        art_institute=art_institute,
    )

    await service.delete_project(project_id)
