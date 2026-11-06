from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    description="REST API to track job applications. Built with FastAPI, SQLAlchemy and Docker.",
    version="1.0.0",
)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.post("/applications", response_model=schemas.ApplicationOut, status_code=201, tags=["applications"])
def create_application(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)


@app.get("/applications", response_model=list[schemas.ApplicationOut], tags=["applications"])
def list_applications(
    status: models.Status | None = None,
    company: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return crud.list_(db, status, company, skip, limit)


@app.get("/applications/stats", response_model=schemas.Stats, tags=["applications"])
def application_stats(db: Session = Depends(get_db)):
    return crud.stats(db)


@app.get("/applications/{app_id}", response_model=schemas.ApplicationOut, tags=["applications"])
def get_application(app_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj


@app.patch("/applications/{app_id}", response_model=schemas.ApplicationOut, tags=["applications"])
def update_application(app_id: int, data: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud.update(db, obj, data)


@app.delete("/applications/{app_id}", status_code=204, tags=["applications"])
def delete_application(app_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")
    crud.delete(db, obj)
