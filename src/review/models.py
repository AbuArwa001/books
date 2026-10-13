from pydantic import BaseModel
from sqlmodel import Column, Integer, String, ForeignKey
from sqlmodel import Basemodel

class Review(BaseModel, table=True):
    __tablename__ = "reviews"

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(String, nullable=False)
    rating: int = Column(Integer, nullable=False)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
