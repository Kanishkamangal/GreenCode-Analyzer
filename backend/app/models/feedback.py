from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    text,
)

from app.database.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    rating = Column(
        Integer,
        nullable=True
    )

    category = Column(
        String(50),
        nullable=False
    )

    feedback_text = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (
        CheckConstraint(
            "rating IS NULL OR (rating >= 1 AND rating <= 5)",
            name="chk_feedback_rating"
        ),
    )