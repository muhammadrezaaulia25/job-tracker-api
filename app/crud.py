from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


def create(db: Session, data: schemas.ApplicationCreate) -> models.Application:
    values = data.model_dump(exclude_none=True)
    obj = models.Application(**values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get(db: Session, app_id: int) -> models.Application | None:
    return db.get(models.Application, app_id)


def list_(
    db: Session,
    status: models.Status | None = None,
    company: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[models.Application]:
    stmt = select(models.Application).order_by(models.Application.id.desc())
    if status:
        stmt = stmt.where(models.Application.status == status)
    if company:
        stmt = stmt.where(models.Application.company.ilike(f"%{company}%"))
    return list(db.scalars(stmt.offset(skip).limit(limit)))


def update(db: Session, obj: models.Application, data: schemas.ApplicationUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: models.Application) -> None:
    db.delete(obj)
    db.commit()


def stats(db: Session) -> schemas.Stats:
    rows = db.execute(
        select(models.Application.status, func.count()).group_by(models.Application.status)
    ).all()
    by_status = {status.value: count for status, count in rows}
    return schemas.Stats(total=sum(by_status.values()), by_status=by_status)
