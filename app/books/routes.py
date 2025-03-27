from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.check_permission import check_permission
from app.dependencies.get_db import get_db
from app.books.schemas import BookCreate, BookSearch, BookUpdate, BookResponse
from app.books.repository import books_repository
from app.users.schemas import TokenPayload
from app.config.roles_permissions_enums import PermissionsEnum


books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.post("/", response_model=BookResponse)
async def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    user: TokenPayload = check_permission([PermissionsEnum.WRITE])
    new_book = await books_repository.create_book(book_data=book, owner_id=user.user_id, db=db)
    return new_book


@books_router.get("/", response_model=list[BookResponse])
async def get_books(
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.READ])
    return await books_repository.get_books(db)


@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book: BookSearch,
    db: AsyncSession = Depends(get_db),
):
    check_permission([PermissionsEnum.READ])
    book_obj = await books_repository.get_book(book, db)
    if not book_obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_obj


@books_router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: AsyncSession = Depends(get_db),
):
    user: TokenPayload = check_permission([PermissionsEnum.UPDT_ANY, PermissionsEnum.UPDT_OWN])
    book = await books_repository.get_book(BookSearch(id=book_id), db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if PermissionsEnum.UPDT_ANY not in user.permissions:
        if user.user_id != book.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden")
    return await books_repository.update_book(book, book_update, db)


@books_router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    user: TokenPayload = check_permission([PermissionsEnum.DLT_ANY, PermissionsEnum.DLT_OWN])
    book = await books_repository.get_book(BookSearch(id=book_id), db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if PermissionsEnum.DLT_ANY not in user.permissions:
        if user.user_id != book.owner_id:
            raise HTTPException(status_code=403, detail="Forbidden")
    await books_repository.delete_book(book, db)
    return {"message": "Book deleted successfully"}
