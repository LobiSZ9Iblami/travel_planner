from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import (
    IDMixin,
    TimestampsMixin
)


class TravelProject(
    Base,
    IDMixin,
    TimestampsMixin
):
    __tablename__ = "travel_projects"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    places: Mapped[list["TravelPlace"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )
