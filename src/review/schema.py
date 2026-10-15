import uuid
from pydantic import BaseModel

class ReviewModel(BaseModel):
    id: uuid.UUID
    content: str
    rating: int
    
