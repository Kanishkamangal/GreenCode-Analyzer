from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.benchmark import (
    BenchmarkCreate,
    BenchmarkResponse,
)

from app.services import benchmark_service

router = APIRouter(
    prefix="/benchmarks",
    tags=["Benchmarks"]
)


# -----------------------------
# Create Benchmark
# -----------------------------
@router.post(
    "/",
    response_model=BenchmarkResponse,
    status_code=201
)
def create_benchmark(
    benchmark: BenchmarkCreate,
    db: Session = Depends(get_db)
):
    return benchmark_service.create_benchmark(db, benchmark)


# -----------------------------
# Get All Benchmarks
# -----------------------------
@router.get(
    "/",
    response_model=list[BenchmarkResponse]
)
def get_all_benchmarks(
    db: Session = Depends(get_db)
):
    return benchmark_service.get_all_benchmarks(db)


# -----------------------------
# Get Benchmark By ID
# -----------------------------
@router.get(
    "/{bench_id}",
    response_model=BenchmarkResponse
)
def get_benchmark(
    bench_id: int,
    db: Session = Depends(get_db)
):
    benchmark = benchmark_service.get_benchmark_by_id(db, bench_id)

    if benchmark is None:
        raise HTTPException(
            status_code=404,
            detail="Benchmark not found."
        )

    return benchmark


# -----------------------------
# Delete Benchmark
# -----------------------------
@router.delete(
    "/{bench_id}"
)
def delete_benchmark(
    bench_id: int,
    db: Session = Depends(get_db)
):
    benchmark = benchmark_service.delete_benchmark(db, bench_id)

    if benchmark is None:
        raise HTTPException(
            status_code=404,
            detail="Benchmark not found."
        )

    return {
        "message": "Benchmark deleted successfully."
    }