from pydantic import BaseModel
from datetime import datetime

from app.schemas.travel_place_schema import TravelPlaceCreate, TravelPlaceResponse


class TravelProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None


class TravelProjectCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None

    places: list[TravelPlaceCreate] = [TravelPlaceCreate]


class TravelProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None


class TravelProjectResponse(TravelProjectBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True


class TravelProjectWithPlacesResponse(TravelProjectResponse):
    places: list[TravelPlaceResponse] = [TravelPlaceResponse]
