from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    role_id: int


class UserSearch(BaseModel):
    email: Optional[str]
    username: Optional[str]
    user_id: Optional[int]


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
