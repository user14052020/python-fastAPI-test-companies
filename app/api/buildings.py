from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from math import radians, cos, sin, asin, sqrt

from app.core.database import SessionLocal
from app.core.security import api_key_auth
from app.models.building import Building
from app.models.organization import Organization
from app.schemas.building import BuildingOut
from app.schemas.organization import OrganizationOut

router = APIRouter(prefix="/buildings", tags=["Buildings"])

# --- Dependency для базы ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Список всех зданий ---
@router.get("/", response_model=List[BuildingOut])
def get_buildings(
    db: Session = Depends(get_db) 
):
    return db.query(Building).all()


# --- Получить здание по ID ---
@router.get("/{building_id}", response_model=BuildingOut)
def get_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    return db.get(Building, building_id)


# --- Список организаций в конкретном здании ---
@router.get("/{building_id}/organizations", response_model=List[OrganizationOut])
def get_organizations_in_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Organization)
        .filter(Organization.building_id == building_id)
        .all()
    )


# --- Поиск зданий в прямоугольной области ---
@router.get("/search/by-area", response_model=List[BuildingOut])
def search_buildings_by_area(
    min_lat: float = Query(..., description="Минимальная широта"),
    max_lat: float = Query(..., description="Максимальная широта"),
    min_lon: float = Query(..., description="Минимальная долгота"),
    max_lon: float = Query(..., description="Максимальная долгота"),
    db: Session = Depends(get_db)
):
    return (
        db.query(Building)
        .filter(Building.latitude.between(min_lat, max_lat))
        .filter(Building.longitude.between(min_lon, max_lon))
        .all()
    )


# --- Поиск организаций по радиусу от точки ---
@router.get("/search/by-radius", response_model=List[OrganizationOut])
def search_organizations_by_radius(
    lat: float = Query(..., description="Центр широта"),
    lon: float = Query(..., description="Центр долгота"),
    radius_km: float = Query(..., description="Радиус в километрах"),
    db: Session = Depends(get_db)
):
    """
    Поиск организаций в радиусе от точки (Haversine formula)
    """
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # радиус Земли в км
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    buildings = db.query(Building).all()
    nearby_building_ids = [
        b.id for b in buildings if haversine(lat, lon, b.latitude, b.longitude) <= radius_km
    ]

    return db.query(Organization).filter(Organization.building_id.in_(nearby_building_ids)).all()
