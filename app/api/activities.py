from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.core.security import api_key_auth
from app.models.activity import Activity
from app.models.organization import Organization
from app.schemas.activity import ActivityOut
from app.schemas.organization import OrganizationOut

router = APIRouter(prefix="/activities", tags=["Activities"])

# --- Dependency для базы ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Проверка глубины вложенности ---
def get_depth(activity: Activity, depth: int = 1) -> int:
    if not activity.parent:
        return depth
    return get_depth(activity.parent, depth + 1)


# --- Создание деятельности ---
@router.post("/", response_model=ActivityOut)
def create_activity(
    name: str,
    parent_id: int | None = None,
    db: Session = Depends(get_db)
):
    parent = None
    if parent_id:
        parent = db.get(Activity, parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent activity not found")
        if get_depth(parent) >= 3:
            raise HTTPException(status_code=400, detail="Maximum activity nesting level is 3")

    activity = Activity(name=name, parent=parent)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


# --- Корневые виды деятельности ---
@router.get("/", response_model=List[ActivityOut])
def get_root_activities(
    db: Session = Depends(get_db)
):
    return db.query(Activity).filter(Activity.parent_id.is_(None)).all()


# --- Получить деятельность по ID ---
@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


# --- Получить все организации по деятельности (рекурсивно) ---
@router.get("/{activity_id}/organizations", response_model=List[OrganizationOut])
def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # рекурсивно собираем все дочерние id
    def get_all_child_ids(act: Activity) -> list[int]:
        ids = [act.id]
        for child in act.children:
            ids.extend(get_all_child_ids(child))
        return ids

    all_ids = get_all_child_ids(activity)
    return db.query(Organization).filter(Organization.activities.any(id__in=all_ids)).all()
