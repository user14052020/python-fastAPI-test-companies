from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.models.organization import Organization
from app.schemas.organization import OrganizationOut  # <- Pydantic схема
from app.core.security import api_key_auth

router = APIRouter(prefix="/organizations", tags=["Organizations"])

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Получить организацию по ID ---
@router.get("/{org_id}", response_model=OrganizationOut)
def get_organization(
    org_id: int,
    db: Session = Depends(get_db)
):
    org = db.get(Organization, org_id)
    if not org:
        return {"error": "Organization not found"}
    return org


# --- Поиск организаций по названию ---
@router.get("/search/", response_model=List[OrganizationOut])
def search_by_name(
    name: str,
    db: Session = Depends(get_db)   
):
    return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()


# --- Список организаций в конкретном здании ---
@router.get("/by-building/{building_id}", response_model=List[OrganizationOut])
def orgs_by_building(
    building_id: int,
    db: Session = Depends(get_db)   
):
    return db.query(Organization).filter_by(building_id=building_id).all()


# --- Список организаций по виду деятельности ---
@router.get("/by-activity/{activity_id}", response_model=List[OrganizationOut])
def orgs_by_activity(
    activity_id: int,
    db: Session = Depends(get_db)    
):
    from app.models.activity import Activity

    activity = db.get(Activity, activity_id)
    if not activity:
        return []

    # рекурсивно собираем все дочерние id
    def get_all_child_ids(act: Activity) -> list[int]:
        ids = [act.id]
        for child in act.children:
            ids.extend(get_all_child_ids(child))
        return ids

    all_ids = get_all_child_ids(activity)

    return db.query(Organization).filter(
        Organization.activities.any(id__in=all_ids)
    ).all()
