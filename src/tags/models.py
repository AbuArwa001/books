from sqlmodel import Column, Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import UUID as uuid
from uuid import uuid4

if TYPE_CHECKING:
    from src.books.models import Book


class BookTagLink(SQLModel, table=True):
    __tablename__ = "book_tag_link"
    book_id: uuid = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid = Field(default=None, foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    
    id: uuid = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    
    
    books: list["Book"] = Relationship(
        back_populates="tags",
        link_model=BookTagLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )