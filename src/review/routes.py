from fastapi import APIRouter, Depends, HTTPException
from src.db import get_session
from src.review.models import Review
from src.review.schema import ReviewModel
from src.review.service import ReviewService


def get_review_service(session=Depends(get_session)):
    return ReviewService(session)

review_service = get_review_service()

router = APIRouter()

@router.post("/reviews/", response_model=ReviewModel)
def create_review(review: ReviewModel, session=Depends(get_session)):
    new_review = review_service.create_review(review)
    
    return new_review

@router.get("/reviews/{review_id}", response_model=ReviewModel)
def get_review(review_id: int, session=Depends(get_session)):
    review = review_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/reviews/{review_id}", response_model=ReviewModel)
def update_review(review_id: int, review: ReviewModel, session=Depends(get_session)):
    updated_review = review_service.update_review(review_id, review)
    return updated_review

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, session=Depends(get_session)):
    review_service.delete_review(review_id)
    return {"message": "Review deleted successfully"}


@router.get("/reviews/", response_model=list[ReviewModel])
def get_all_reviews(session=Depends(get_session)):
    reviews = review_service.get_all_reviews()
    return reviews