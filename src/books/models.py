# from pydantic import BaseModel,
from datetime import date, datetime, timezone
from uuid import UUID as uuid
from uuid import uuid4
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid = Field(
        default_factory=uuid4,
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            index=True,
        ),
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_id: Optional[uuid] = Field(
        default=None,
        foreign_key="users.uid",
        # sa_column=Column(
        #     pg.UUID,
        #     nullable=True,
        # ),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            onupdate=lambda: datetime.now(timezone.utc),
        ),
    )

    def __repr__(self):
            return (
                f"Book(title={self.title}, "
                f"author={self.author}, "
                f"publisher={self.publisher}, "
                f"published_date={self.published_date}, "
                f"page_count={self.page_count}, "
                f"language={self.language})"
            )