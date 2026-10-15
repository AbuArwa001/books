from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel, String
from uuid import UUID as uuid
from uuid import uuid4

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: uuid = Field(default=uuid4(), primary_key=True)
    content: str = Field(default=None, nullable=False)
    rating: int = Field(default=None, nullable=False)
    books_id: uuid = Field(default=None, foreign_key="books.uid")
    books: "Book" = Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"Review(id={self.id},\
        content={self.content}, \
        rating={self.rating}, \
        books_id={self.books_id})"