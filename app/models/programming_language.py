from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class ProgrammingLanguage(Base):
    __tablename__ = "programming_language"

    lang_id = Column(Integer, primary_key=True, index=True)
    lang_name = Column(String(30), unique=True, nullable=False)
    compiler = Column(String(100), nullable=False)
    version = Column(String(30), nullable=False)
    compile_command = Column(String(255), nullable=True)
    run_command = Column(String(255), nullable=False)
    
    analyses = relationship("Analysis", back_populates="language")