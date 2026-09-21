from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BenchmarkCreate(BaseModel):
    bench_name: str
    bench_type: str
    category: str


class BenchmarkResponse(BaseModel):
    bench_id: int
    bench_name: str
    bench_type: str
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BenchmarkResponse(BaseModel):
    bench_id: int
    bench_name: str
    folder_name: str
    bench_type: str
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)