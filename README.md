# Job Application Tracker API

REST API for tracking job applications (company, position, status, notes).
Built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL** and **Docker**.

## Features
- Full CRUD for job applications
- Filter by status or company, with pagination
- Statistics endpoint (total and count per status)
- Input validation with Pydantic, automatic Swagger docs
- Automated tests with pytest
- Runs with SQLite locally or PostgreSQL via Docker Compose

## Run with Docker
```bash
docker compose up --build
```
Open http://localhost:8000/docs

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run tests
```bash
pytest
```

## Endpoints
| Method | Path | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /applications | Create an application |
| GET | /applications | List (filter: `status`, `company`; paging: `skip`, `limit`) |
| GET | /applications/stats | Totals per status |
| GET | /applications/{id} | Get one |
| PATCH | /applications/{id} | Partial update |
| DELETE | /applications/{id} | Delete |

## Example
```bash
curl -X POST http://localhost:8000/applications \
  -H "Content-Type: application/json" \
  -d '{"company":"Acme","position":"Python Developer","status":"applied"}'
```

## Tech stack
Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, Docker, pytest
