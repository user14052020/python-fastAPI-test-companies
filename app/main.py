from fastapi import FastAPI, Security

from app.api import organizations, buildings, activities
from app.core.security import api_key_auth


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
