from typing import Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str


class RoleRead(BaseModel):
    role_id: Optional[int] = None
    name: Optional[str] = None
