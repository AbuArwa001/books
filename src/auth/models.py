from sqlmodel import SQLModel, Field, Column
from datetime import date, datetime
from uuid import uuid4, UUID as uuid
import sqlalchemy.dialects.postgresql as pg

"""
class User:
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
"""


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, index=True, default=uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        exclude=True,
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
        ),
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )


def __repr__(self):
    return f"User(username={self.username}, \
        email={self.email}, \
        first_name={self.first_name}, \
        last_name={self.last_name}, \
        updated_at={self.updated_at}, \
        is_verified={self.is_verified})"
