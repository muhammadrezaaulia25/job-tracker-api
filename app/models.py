import enum
from datetime import date

from sqlalchemy import Date, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Status(str, enum.Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company: Mapped[str] = mapped_column(String(120), index=True)
    position: Mapped[str] = mapped_column(String(120))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.applied)
    applied_on: Mapped[date] = mapped_column(Date, default=date.today)
    job_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
