from pydantic import BaseModel
from datetime import datetime


class TravelPlaceBase(BaseModel):
    external_place_id: str
    title: str
    notes: str | None = None
    visited: bool = False


class TravelPlaceCreate(BaseModel):
    external_place_id: str
    title: str
    notes: str | None = None


class TravelPlaceUpdate(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class TravelPlaceResponse(TravelPlaceBase):
    id: int
    travel_project_id: int
    create_date: datetime
    update_date: datetime
    visited_at: datetime | None = None

    class Config:
        from_attributes = True


class TravelPlaceListResponse(BaseModel):
    items: list[TravelPlaceResponse]
