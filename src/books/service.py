

from src.books.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel

class BookService:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        new_book = Book(**book_data.dict())
        self.db_session.add(new_book)
        await self.db_session.commit()
        await self.db_session.refresh(new_book)
        return new_book
    async def get_book(self, book_id, session: AsyncSession):
        book = await self.db_session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")
        return book
    async def update_book(self, book_id, book_data:BookUpdateModel, session: AsyncSession):
        book = await self.db_session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")
        for key, value in book_data.dict(exclude_unset=True).items():
            setattr(book, key, value)
        await self.db_session.commit()
        await self.db_session.refresh(book)
        return book
    async def delete_book(self, book_id, session: AsyncSession):
        book = await self.db_session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")
        await self.db_session.delete(book)
        await self.db_session.commit()

    async def get_all_books(self, session: AsyncSession):
        books = await self.db_session.execute("SELECT * FROM books")
        return books.fetchall()