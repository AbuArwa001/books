from sqlmodel import Column, Field, SQLModel, Relationship
from typing import List, Optional
from src.books.models import Book
from uuid import UUID as uuid
from uuid import uuid4


class BookTagLink(SQLModel, table=True):
    __tablename__ = "book_tag_link"
    book_id: uuid = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid = Field(default=None, foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: uuid = Field(default=uuid4(), primary_key=True)
    name: str = Field(unique=True, nullable=False)
    books_id: Optional[List[uuid]] = Field(default=None, foreign_key="books.uid")
    books: list["Book"] = Relationship(
        back_populates="tags",
        link_model="BookTagLink",
        sa_relationship_kwargs={"lazy": "selectin"},
    )