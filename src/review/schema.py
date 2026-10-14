from pydantic import BaseModel, Field

class ReviewModel(BaseModel):
    id: int 
    content: str 
    rating: int 
    books_id: int
    
