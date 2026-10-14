from pydantic import BaseModel
from typing import List

class TagsSchema(BaseModel):
    id: int
    name: str
    books: List
