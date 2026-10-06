# from pydantic import BaseModel, 
from sqlmodel import SQLModel,Field, Column
from datetime import date, datetime
from uuid import uuid4, UUID as uuid
import sqlalchemy.dialects.postgresql as pg


class Book(SQLModel, table=True):
        __tablename__ = "books"
        uid: uuid = Field(
                sa_column=Column(
                pg.UUID,     
                nullable=False,
                primary_key=True,
                index=True,
                default=uuid4
                )
                )
        title: str
        author: str
        publisher: str
        published_date: date
        page_count: int
        language: str
        created_at: datetime = Field(default_factory=datetime.utcnow)
        updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

        def __repr__(self):
                return f"Book(title={self.title}, author={self.author}, publisher={self.publisher}, published_date={self.published_date}, page_count={self.page_count}, language={self.language})"
        