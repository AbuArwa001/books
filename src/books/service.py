from src.books.models import Book
from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book

class BookService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        self.db_session.add(new_book)
        await self.db_session.commit()
        await self.db_session.refresh(new_book)
        return new_book

    async def get_book(self, book_id:str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await self.db_session.exec(statement)
        book = result.scalars().first()
        if not book:
            raise ValueError("Book not found")
        return book
    async def update_book(self, book_id:str, book_data:BookUpdateModel, session: AsyncSession):
        book = self.get_book(book_id, session)
        if not book:
            raise ValueError("Book not found")
        book_data_dict = book_data.model_dump(exclude_unset=True)
        for key, value in book_data_dict.items():
            setattr(book, key, value)
        await self.db_session.commit()
        await self.db_session.refresh(book)
        return book
    async def delete_book(self, book_id:str, session: AsyncSession):
        book = self.get_book(book_id, session)
        if not book:
            raise ValueError("Book not found")
        await self.db_session.delete(book)
        await self.db_session.commit()

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await self.db_session.exec(statement)
        books = result.scalars().all()
        return books