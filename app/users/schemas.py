from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    role_id: int


class UserSearch(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
