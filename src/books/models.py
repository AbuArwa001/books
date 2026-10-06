# from pydantic import BaseModel, 
from sqlmodel import SQLModel,Field, Column
from datetime import datetime
from uuid import uuid4, UUID as uuid
import sqlalchemy.dialects.postgresql as pg


class Book(SQLModel, table=True):
        __tablename__ = "books"
        uid: uuid = Field(
                sa_column=Column(
                pg.UUID,
                nullable=False,
                primary_key=True,
                )
                )
        title: str
        author: str
        publisher: str
        published_date: str
        page_count: int
        language: str
        created_at: datetime = Field(default_factory=datetime.utcnow)
        updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
