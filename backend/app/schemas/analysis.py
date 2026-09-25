from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any, Optional

class AnalysisCreate(BaseModel):
    user_id: int
    lang_id: int
    comparison_id: Optional[int] = None
    analysis_type: str = "predefined"

    bench_id: Optional[int] = None
    
    bench_size: Optional[str] = None

    custom_category: Optional[str] = None
    custom_benchmark_name: Optional[str] = None
    custom_description: Optional[str] = None 
    benchmark_metadata: Optional[dict[str, Any]] = None

    workload_type: Optional[str] = None

    input_size: Optional[int] = None

class AnalysisComparisonCreate(BaseModel):
    user_id: int
    bench_id: int
    lang_ids: list[int]
    bench_size: str


class CustomAnalysisComparisonCreate(BaseModel):
    user_id: int

    custom_category: str
    custom_benchmark_name: str
    custom_description: Optional[str] = None

    # --------------------------------------------------
    # Workload configuration
    # --------------------------------------------------

    workload_type: Optional[str] = None

    input_size: Optional[int] = None

    # Optional user-provided workload
    custom_input: Optional[str] = None

    reference_lang_id: int
    reference_code: str

    target_lang_ids: list[int]

class ReferenceCodeAnalysisRequest(BaseModel):
    reference_code: str

class AnalysisResponse(BaseModel):
    analysis_id: int
    comparison_id: Optional[int] = None
    user_id: int
    analysis_type: str

    bench_id: Optional[int] = None
    lang_id: int
    bench_size: Optional[str] = None

    custom_category: Optional[str] = None
    custom_benchmark_name: Optional[str] = None
    custom_description: Optional[str] = None
    benchmark_metadata: Optional[dict[str, Any]] = None
    workload_type: Optional[str] = None
    input_size: Optional[int] = None

    execution_time: float
    cpu_usage: float
    memory_usage: float
    energy_consumption: float | None

    green_score: float | None = None
    green_score_label: str | None = None

    output_verified: Optional[bool] = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )