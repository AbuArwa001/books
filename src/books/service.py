from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book

from .schemas import BookCreateModel, BookUpdateModel


class BookService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_book(self, book_data: BookCreateModel, user_id: str):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.user_id = user_id
        self.db_session.add(new_book)
        await self.db_session.commit()
        await self.db_session.refresh(new_book)
        return new_book

    async def get_book(self, book_id: str):
        statement = select(Book).where(Book.uid == book_id)
        result = await self.db_session.exec(statement)
        book = result.first()
        if not book:
            return None
        return book

    async def update_book(
        self, book_id: str, book_data: BookUpdateModel
    ):
        book = await self.get_book(book_id)
        if not book:
            return None
        book_data_dict = book_data.model_dump(exclude_unset=True)
        for key, value in book_data_dict.items():
            setattr(book, key, value)
        await self.db_session.commit()
        await self.db_session.refresh(book)
        return book

    async def delete_book(self, book_id: str):
        book = await self.get_book(book_id)
        if not book:
            return None
        await self.db_session.delete(book)
        await self.db_session.commit()

    async def get_all_books(self):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await self.db_session.exec(statement)
        books = result.all()
        return books
    async def get_user_books(self, user_id: str):
        statement = select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        result = await self.db_session.exec(statement)
        books = result.all()
        return books