from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComparisonResponse(BaseModel):
    comparison_id: int
    user_id: int

    comparison_type: str

    bench_id: Optional[int] = None
    bench_size: Optional[str] = None
    input_size: Optional[int] = None

    custom_category: Optional[str] = None
    custom_benchmark_name: Optional[str] = None
    workload_type: Optional[str] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )