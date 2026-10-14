from sqlmodel import Column, Field, ForeignKey, Integer, SQLModel, String

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: int = Field(default=None, primary_key=True)
    content: str = Field(default=None, nullable=False)
    rating: int = Field(default=None, nullable=False)
    books_id: int = Field(default=None, foreign_key="books.uid")

    def __repr__(self):
        return f"Review(id={self.id},\
        content={self.content}, \
        rating={self.rating}, \
        books_id={self.books_id})"