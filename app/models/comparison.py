from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"

    comparison_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True,
    )

    bench_id = Column(
        Integer,
        ForeignKey("benchmark.bench_id"),
        nullable=True,
    )

    comparison_type = Column(
        String,
        nullable=False,
        default="predefined",
    )

    bench_size = Column(
        String,
        nullable=True,
    )

    input_size = Column(
        Integer,
        nullable=True,
    )

    custom_category = Column(
        String,
        nullable=True,
    )

    custom_benchmark_name = Column(
        String,
        nullable=True,
    )

    workload_type = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    analyses = relationship(
        "Analysis",
        back_populates="comparison",
        cascade="all, delete-orphan",
    )