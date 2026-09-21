from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def create_feedback(
    db: Session,
    feedback: FeedbackCreate
):

    new_feedback = Feedback(
        user_id=feedback.user_id,
        rating=feedback.rating,
        category=feedback.category,
        feedback_text=feedback.feedback_text,
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback


def get_all_feedback(db: Session):

    return (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .all()
    )