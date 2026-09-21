from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.comparison_service import (
    get_comparison,
    get_comparisons_by_user,
)


router = APIRouter(
    prefix="/comparisons",
    tags=["Comparisons"],
)


# =====================================================
# GET ALL COMPARISONS FOR USER
# =====================================================

@router.get("/user/{user_id}")
def read_user_comparisons(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_comparisons_by_user(
        db,
        user_id,
    )


# =====================================================
# GET SINGLE COMPARISON
# =====================================================

@router.get("/{comparison_id}")
def read_comparison(
    comparison_id: int,
    db: Session = Depends(get_db),
):
    comparison_data = get_comparison(
        db,
        comparison_id,
    )

    if comparison_data is None:
        raise HTTPException(
            status_code=404,
            detail="Comparison not found",
        )

    return comparison_data