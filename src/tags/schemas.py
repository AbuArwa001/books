from pydantic import BaseModel
from typing import List
from uuid import UUID as uuid
from uuid import uuid4

class TagsSchema(BaseModel):
    id: uuid
    name: str
    books: List
