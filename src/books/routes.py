from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

# from src.books.book_data import books
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session

book_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    print("User details from access token:", user_details)
    book_service = BookService(session)
    return await book_service.get_all_books()


@book_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Book
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
) -> Book:
    book_service = BookService(session)
    new_book = await book_service.create_book(book_data)
    return new_book


@book_router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: str, session: AsyncSession = Depends(get_session)
) -> Book:

    book_service = BookService(session)
    book = await book_service.get_book(book_id)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found"
    )


@book_router.patch("/{book_id}", response_model=Book)
async def update_book(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> Book:
    book_service = BookService(session)
    book = await book_service.update_book(book_id, book_update_data)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found"
    )


@book_router.delete(
    "/{book_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: str, session: AsyncSession = Depends(get_session)
):
    book_service = BookService(session)
    book = await book_service.delete_book(book_id)
    if book:
        return {"message": "Book deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found"
    )
