from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Double,
    text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from app.models.comparison import Comparison
from app.database.database import Base


class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, index=True)
    comparison_id = Column(
        Integer,
        ForeignKey("comparisons.comparison_id"),
        nullable=True,
        index=True,
    )
    comparison = relationship(
        "Comparison",
        back_populates="analyses",
    )
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    bench_id = Column(Integer, ForeignKey("benchmark.bench_id"), nullable=True)
    lang_id = Column(Integer, ForeignKey("programming_language.lang_id"), nullable=False)
    analysis_type = Column(String(20),nullable=False)
    bench_size = Column(String(20), nullable=True)
    # Only required for custom benchmarks
    custom_category = Column(
        String(100),
        nullable=True
    )

    custom_benchmark_name = Column(
        String(150),
        nullable=True
    )

    custom_description = Column(
        String(500),
        nullable=True
    )
    benchmark_metadata = Column(
        JSON,
        nullable=True
    )

    workload_type = Column(
        String(50),
        nullable=True
    )
    
    # Custom: actual workload size
    input_size = Column(
        Integer,
        nullable=True
    )
    execution_time = Column(Double, nullable=False)
    cpu_usage = Column(Double, nullable=False)
    memory_usage = Column(Double, nullable=False)
    energy_consumption = Column(Double,nullable=True)
    green_score = Column(Double, nullable=True)
    green_score_label = Column(String(20), nullable=True)
    output_verified = Column(Boolean, server_default=text("true"))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    user = relationship("User", back_populates="analyses")
    benchmark = relationship("Benchmark", back_populates="analyses")
    language = relationship("ProgrammingLanguage", back_populates="analyses")

    report = relationship(
        "Report",
        back_populates="analysis",
        uselist=False,
    )