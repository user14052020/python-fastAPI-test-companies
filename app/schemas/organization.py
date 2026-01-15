from pydantic import BaseModel
from typing import List

class OrganizationOut(BaseModel):
    id: int
    name: str
    phones: List[str]
    building_id: int

    class Config:
        from_attributes = True
