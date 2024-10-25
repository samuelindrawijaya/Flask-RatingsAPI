from app.config.connector import db
from app.models.reviewModel import Review
from datetime import datetime

class ReviewDAL:
    @staticmethod
    def create_review(content, user_id):
        review = Review(content=content, user_id=user_id, created_at=datetime.now())
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_review_by_id(review_id):
        return db.session.get(Review, review_id)

    @staticmethod
    def get_reviews_by_user_id(user_id):
        return Review.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_review(review_id, new_content):
        review = db.session.get(Review, review_id)
        if review:
            review.content = new_content
            db.session.commit()
        return review

    @staticmethod
    def delete_review(review_id):
        review = db.session.get(Review, review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False

    @staticmethod
    def list_reviews():
        return Review.query.all()
