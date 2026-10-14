from pydantic import BaseModel

class TagsSchema(BaseModel):
    id: int
    name: str
