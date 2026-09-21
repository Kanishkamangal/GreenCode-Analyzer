from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, index=True)

    analysis_id = Column(
        Integer,
        ForeignKey("analysis.analysis_id"),
        nullable=False
    )

    report_name = Column(String(100), nullable=False)
    report_type = Column(String(20), nullable=False)
    file_path = Column(String(255), nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    analysis = relationship("Analysis", back_populates="report")