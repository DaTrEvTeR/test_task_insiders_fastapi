from typing import Optional
from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str

    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None


class BookSearch(BookUpdate):
    id: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = ""
    owner_id: int
