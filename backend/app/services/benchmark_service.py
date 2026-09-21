from sqlalchemy.orm import Session

from app.models.benchmark import Benchmark
from app.schemas.benchmark import BenchmarkCreate


def get_all_benchmarks(db: Session):
    return db.query(Benchmark).all()


def get_benchmark_by_id(db: Session, bench_id: int):
    return db.query(Benchmark).filter(
        Benchmark.bench_id == bench_id
    ).first()


def create_benchmark(db: Session, benchmark: BenchmarkCreate):

    new_benchmark = Benchmark(
        bench_name=benchmark.bench_name,
        folder_name=benchmark.folder_name,
        bench_type=benchmark.bench_type,
        category=benchmark.category
    )
    db.add(new_benchmark)
    db.commit()
    db.refresh(new_benchmark)

    return new_benchmark


def delete_benchmark(db: Session, bench_id: int):

    benchmark = get_benchmark_by_id(db, bench_id)

    if not benchmark:
        return None

    db.delete(benchmark)
    db.commit()
    return benchmark

def update_benchmark(
    db: Session,
    bench_id: int,
    benchmark: BenchmarkCreate
):
    existing = get_benchmark_by_id(db, bench_id)

    if not existing:
        return None

    existing.bench_name = benchmark.bench_name
    existing.folder_name = benchmark.folder_name
    existing.bench_type = benchmark.bench_type
    existing.category = benchmark.category

    db.commit()
    db.refresh(existing)

    return existing