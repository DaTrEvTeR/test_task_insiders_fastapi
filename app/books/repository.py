from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.book import Book
from app.books.schemas import BookCreate, BookUpdate, BookSearch


class BooksRepository:
    async def create_book(self, book_data: BookCreate, owner_id: int, db: AsyncSession) -> Book:
        book = Book(
            title=book_data.title, author=book_data.author, description=book_data.description, owner_id=owner_id
        )
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    async def get_book(self, model: BookSearch, db: AsyncSession) -> Book | None:
        statement = select(Book)
        if model.id:
            statement = statement.filter_by(id=model.id)
        if model.author:
            statement = statement.filter_by(username=model.author)
        if model.description:
            statement = statement.filter_by(description=model.description)
        if model.title:
            statement = statement.filter_by(title=model.title)
        result = await db.execute(statement)
        return result.unique().scalar_one_or_none()

    async def get_books(self, db: AsyncSession) -> list[Book]:
        result = await db.execute(select(Book))
        return result.unique().scalars().all()

    async def update_book(self, book: Book, model: BookUpdate, db: AsyncSession) -> Book:
        if model.title:
            book.title = model.title
        if model.author:
            book.author = model.author
        if model.description:
            book.description = model.description
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    async def delete_book(self, book: Book, db: AsyncSession) -> None:
        await db.delete(book)
        await db.commit()


books_repository = BooksRepository()
