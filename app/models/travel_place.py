from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import (
    IDMixin,
    TimestampsMixin
)


class TravelPlace(
    Base,
    IDMixin,
    TimestampsMixin
):
    __tablename__ = "travel_places"

    travel_project_id: Mapped[int] = mapped_column(
        ForeignKey("travel_projects.id"),
        nullable=False
    )
    external_place_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    visited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped["TravelProject"] = relationship(
        back_populates="places"
    )
