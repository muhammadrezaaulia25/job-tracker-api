from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from .models import Status


class ApplicationBase(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    position: str = Field(min_length=1, max_length=120)
    status: Status = Status.applied
    applied_on: date | None = None
    job_url: str | None = None
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=120)
    position: str | None = Field(default=None, min_length=1, max_length=120)
    status: Status | None = None
    applied_on: date | None = None
    job_url: str | None = None
    notes: str | None = None


class ApplicationOut(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    applied_on: date


class Stats(BaseModel):
    total: int
    by_status: dict[str, int]
