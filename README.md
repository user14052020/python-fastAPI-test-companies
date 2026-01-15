# Organizations Directory API

<img width="1920" height="1187" alt="Screenshot 2026-01-15 at 12 57 07" src="https://github.com/user-attachments/assets/f056a7d1-ad09-4755-95c7-d40ae06c12bc" />


REST API for organizations, buildings, and activities with API key auth.

## Stack

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Postgres

## Environment

Create `.env` based on `.env.example` and fill values:

- `API_KEY` - static API key for requests (header `X-API-Key`)
- `DATABASE_URL` - SQLAlchemy URL
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Run with Docker

Build and start services:

```bash
docker compose up --build
```

API will be available at `http://localhost:8000`.

## First run (Docker)

Run commands inside the API service:

```bash
docker compose run --rm api alembic revision --autogenerate -m "initial"
docker compose run --rm api alembic upgrade head
docker compose run --rm api python -m app.seed
```

If a migration already exists in `alembic/versions`, you can skip the first step.

## API Docs

- Swagger UI: `http://localhost:8000/docs`

## Main Endpoints

- `GET /organizations/{org_id}` - organization by id
- `GET /organizations/search/?name=...` - search by name
- `GET /organizations/by-building/{building_id}` - organizations in building
- `GET /organizations/by-activity/{activity_id}` - organizations by activity (recursive)
- `GET /buildings` - list buildings
- `GET /buildings/{building_id}` - building by id
- `GET /buildings/{building_id}/organizations` - organizations in building
- `GET /buildings/search/by-area?min_lat=...&max_lat=...&min_lon=...&max_lon=...`
- `GET /buildings/search/by-radius?lat=...&lon=...&radius_km=...`
- `GET /activities` - root activities
- `GET /activities/{activity_id}` - activity by id
- `GET /activities/{activity_id}/organizations` - organizations by activity (recursive)
- `POST /activities?name=...&parent_id=...` - create activity (max depth 3)

All endpoints require header `X-API-Key: <API_KEY>`.
