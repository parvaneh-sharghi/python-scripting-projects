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