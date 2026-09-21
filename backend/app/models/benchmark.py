from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Benchmark(Base):
    __tablename__ = "benchmark"

    bench_id = Column(Integer, primary_key=True, index=True)
    bench_name = Column(String(100), nullable=False)
    folder_name = Column(
        String(100),
        unique=True,
        nullable=False
    )
    bench_type = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    analyses = relationship("Analysis", back_populates="benchmark")