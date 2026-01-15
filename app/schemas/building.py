from pydantic import BaseModel

class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingOut(BuildingBase):
    id: int

    class Config:
        from_attributes = True
