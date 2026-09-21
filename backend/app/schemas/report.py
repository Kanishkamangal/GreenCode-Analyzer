# from pydantic import BaseModel, ConfigDict
# from datetime import datetime


# class ReportCreate(BaseModel):
#     analysis_id: int
#     report_name: str
#     report_type: str
#     file_path: str


# class ReportResponse(BaseModel):
#     report_id: int
#     analysis_id: int
#     report_name: str
#     report_type: str
#     file_path: str
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportMetadata(BaseModel):
    benchmark_task: str
    category: Optional[str] = None
    analysis_type: str

    language: str

    input_size: Optional[int] = None
    bench_size: Optional[str] = None
    workload_type: Optional[str] = None

    execution_date: datetime

    runtime: Optional[str] = None
    compiler: Optional[str] = None


class ReportMetrics(BaseModel):
    execution_time: float
    cpu_usage: float
    memory_usage: float
    energy_consumption: Optional[float] = None

    green_score: Optional[float] = None
    green_score_label: Optional[str] = None

    output_verified: Optional[bool] = None


class ReportDTO(BaseModel):
    report_title: str

    analysis_id: int
    user_id: int

    metadata: ReportMetadata
    metrics: ReportMetrics

    rank: Optional[int] = None
    total_comparisons: Optional[int] = None

class ComparisonReportResult(BaseModel):
    analysis_id: int

    language: str
    compiler: Optional[str] = None
    version: Optional[str] = None

    execution_time: float
    cpu_usage: float
    memory_usage: float

    energy_consumption: Optional[float] = None

    green_score: Optional[float] = None
    green_score_label: Optional[str] = None

    output_verified: Optional[bool] = None

    created_at: datetime

    input_size: Optional[int] = None
    bench_size: Optional[str] = None
    workload_type: Optional[str] = None


class ComparisonReportDTO(BaseModel):
    comparison_id: int
    user_id: int

    comparison_type: str

    benchmark_name: str
    category: Optional[str] = None

    bench_size: Optional[str] = None
    input_size: Optional[int] = None
    workload_type: Optional[str] = None

    created_at: datetime

    results: list[ComparisonReportResult]