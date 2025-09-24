from pydantic import BaseModel,Field
from typing import Optional,Literal
from datetime import datetime

class VulnCreate(BaseModel):
    title: str= Field(...,min_length=2)
    severity: Optional[Literal["low", "medium", "high", "critical"]] = "medium"
    notes: Optional[str] = None

class VulnRead(BaseModel):
    id: int
    title: str
    severity: str
    status: str
    notes: Optional[str] = None
    discovered_at: datetime
    archived: bool

class VulnUpdate(BaseModel):
    # all fields are optional for partial update
    title: Optional[str] = None
    severity: Optional[Literal["low", "medium", "high", "critical"]] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    archived: Optional[bool] = None