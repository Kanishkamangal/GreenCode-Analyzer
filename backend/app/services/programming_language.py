from sqlalchemy.orm import Session

from app.models.programming_language import ProgrammingLanguage


def get_all_languages(db: Session):
    return db.query(ProgrammingLanguage).all()


def get_language_by_id(db: Session, lang_id: int):
    return db.query(ProgrammingLanguage).filter(
        ProgrammingLanguage.lang_id == lang_id
    ).first()


def get_language_by_name(db: Session, lang_name: str):
    return db.query(ProgrammingLanguage).filter(
        ProgrammingLanguage.lang_name == lang_name
    ).first()