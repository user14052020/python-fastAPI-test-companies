import os
from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.api import organizations, buildings, activities

# =========================
# API KEY AUTH (OpenAPI)
# =========================

API_KEY_NAME = "X-API-Key"

# Swagger поймёт это как security scheme и даст кнопку Authorize
api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def api_key_auth(api_key: str = Security(api_key_scheme)) -> str:
    """
    Проверка API ключа.
    Ключ хранится в переменной окружения API_KEY (например в .env).
    """
    expected_key = os.getenv("API_KEY", "SECRET_API_KEY")

    if api_key == expected_key:
        return api_key

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )


# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="Organizations Directory API",
    description="REST API для справочника организаций, зданий и деятельностей",
    version="1.0.0",
)

# =========================
# ROUTERS (secured globally)
# =========================

app.include_router(organizations.router, dependencies=[Security(api_key_auth)])
app.include_router(buildings.router, dependencies=[Security(api_key_auth)])
app.include_router(activities.router, dependencies=[Security(api_key_auth)])