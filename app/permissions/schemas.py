from typing import Optional
from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str


class PermissionRead(BaseModel):
    permission_id: Optional[int] = None
    name: Optional[str] = None
