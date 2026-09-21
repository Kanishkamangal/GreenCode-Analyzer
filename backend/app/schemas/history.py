from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HistoryItem(BaseModel):
    analysis_id: int
    user_id: int

    analysis_type: str

    benchmark_name: str
    category: Optional[str] = None
    language: str

    bench_size: Optional[str] = None
    comparison_id: Optional[int] = None
    input_size: Optional[int] = None
    workload_type: Optional[str] = None

    execution_time: float
    cpu_usage: float
    memory_usage: float
    energy_consumption: Optional[float] = None

    green_score: Optional[float] = None
    green_score_label: Optional[str] = None

    output_verified: Optional[bool] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    total: int