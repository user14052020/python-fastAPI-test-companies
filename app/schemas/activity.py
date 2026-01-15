from pydantic import BaseModel
from typing import List, Optional

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityOut(ActivityBase):
    id: int
    children: List["ActivityOut"] = []

    class Config:
        from_attributes = True


ActivityOut.model_rebuild()
