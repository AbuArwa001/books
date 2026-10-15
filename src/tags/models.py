from sqlmodel import Column, Field, SQLModel, Relationship

from src.books.models import Book
from uuid import UUID as uuid
from uuid import uuid4


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: uuid = Field(default=uuid4(), primary_key=True)
    name: str = Field(sa_column=Column("name", nullable=False, unique=True))
    books: list["Book"] = Relationship(
        back_populates="tags",
        # link_model="BookTagLink",
        sa_relationship_kwargs={"lazy": "selectin"},
    )