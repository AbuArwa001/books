from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.review.models import Review
from src.review.schema import ReviewModel



class ReviewService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create_review(self, review_data: ReviewModel):
        review = Review(**review_data.dict())
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review

    def get_review(self, review_id: int):
        review = self.session.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    def update_review(self, review_id: int, review_data: ReviewModel):
        review = self.get_review(review_id)
        for key, value in review_data.dict().items():
            setattr(review, key, value)
        self.session.commit()
        self.session.refresh(review)
        return review

    def delete_review(self, review_id: int):
        review = self.get_review(review_id)
        self.session.delete(review)
        self.session.commit()