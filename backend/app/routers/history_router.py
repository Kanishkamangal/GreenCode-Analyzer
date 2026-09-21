from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.history import (
    HistoryItem,
    HistoryListResponse,
)
from app.services import history_service


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get(
    "/user/{user_id}",
    response_model=HistoryListResponse,
)
def get_history_by_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return history_service.get_history_by_user(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{analysis_id}",
    response_model=HistoryItem,
)
def get_history_item(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    item = history_service.get_history_item(
        db=db,
        analysis_id=analysis_id,
    )

    if item is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="History record not found.",
        )

    return item