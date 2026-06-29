from fastapi import APIRouter, Depends, status

from app.schemas.travel_place_schema import (
    TravelPlaceCreate,
    TravelPlaceUpdate,
    TravelPlaceResponse,
    TravelPlaceListResponse,
)
from app.uow.uow import UnitOfWork, get_uow
from app.services.travel_place_service import TravelPlaceService
from app.external_api.art_institute import (
    ArtInstituteClient,
    get_art_institute_client,
)


router = APIRouter(prefix="/projects", tags=["places"])


@router.post(
    "/{project_id}/places",
    response_model=TravelPlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_place(
    project_id: int,
    data: TravelPlaceCreate,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelPlaceResponse:

    service = TravelPlaceService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.add_place(project_id, data)


@router.get(
    "/{project_id}/places",
    response_model=TravelPlaceListResponse,
)
async def list_places(
    project_id: int,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelPlaceListResponse:

    service = TravelPlaceService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.list_places(project_id)


@router.get(
    "/{project_id}/places/{place_id}",
    response_model=TravelPlaceResponse,
)
async def get_place(
    project_id: int,
    place_id: str,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelPlaceResponse:

    service = TravelPlaceService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.get_place(project_id, place_id)


@router.patch(
    "/{project_id}/places/{place_id}",
    response_model=TravelPlaceResponse,
)
async def update_place(
    project_id: int,
    place_id: int,
    data: TravelPlaceUpdate,
    uow: UnitOfWork = Depends(get_uow),
    art_institute: ArtInstituteClient = Depends(get_art_institute_client),
) -> TravelPlaceResponse:

    service = TravelPlaceService(
        uow=uow,
        art_institute=art_institute,
    )

    return await service.update_place(place_id, data)
