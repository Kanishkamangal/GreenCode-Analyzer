from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse
)

from app.services import feedback_service


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=201
)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):

    if (
        feedback.rating is None
        and not feedback.feedback_text
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Please provide a rating "
                "or feedback message."
            )
        )

    return feedback_service.create_feedback(
        db,
        feedback
    )


@router.get(
    "/",
    response_model=list[FeedbackResponse]
)
def get_feedback(
    db: Session = Depends(get_db)
):

    return feedback_service.get_all_feedback(db)