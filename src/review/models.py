from sqlmodel import Column, ForeignKey, Integer, SQLModel, String

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(String, nullable=False)
    rating: int = Column(Integer, nullable=False)
    books_id: int = Column(Integer, ForeignKey("books.uid"), nullable=False)

    def __repr__(self):
        return f"Review(id={self.id},\
        content={self.content}, \
        rating={self.rating}, \
        books_id={self.books_id})"