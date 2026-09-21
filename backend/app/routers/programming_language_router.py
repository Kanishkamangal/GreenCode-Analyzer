from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.programming_language import (
    ProgrammingLanguageResponse,
)

from app.services import programming_language_service

router = APIRouter(
    prefix="/languages",
    tags=["Programming Languages"]
)


# -----------------------------------
# Get All Programming Languages
# -----------------------------------
@router.get(
    "/",
    response_model=list[ProgrammingLanguageResponse]
)
def get_all_languages(
    db: Session = Depends(get_db)
):
    return programming_language_service.get_all_languages(db)


# -----------------------------------
# Get Programming Language By ID
# -----------------------------------
@router.get(
    "/{lang_id}",
    response_model=ProgrammingLanguageResponse
)
def get_language_by_id(
    lang_id: int,
    db: Session = Depends(get_db)
):

    language = programming_language_service.get_language_by_id(
        db,
        lang_id
    )

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Programming language not found."
        )

    return language


# -----------------------------------
# Get Programming Language By Name
# -----------------------------------
@router.get(
    "/name/{lang_name}",
    response_model=ProgrammingLanguageResponse
)
def get_language_by_name(
    lang_name: str,
    db: Session = Depends(get_db)
):

    language = programming_language_service.get_language_by_name(
        db,
        lang_name
    )

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Programming language not found."
        )

    return language