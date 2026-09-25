from typing import Optional

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.benchmark import Benchmark
from app.models.comparison import Comparison
from app.models.programming_language import ProgrammingLanguage
from app.schemas.report import (
    ComparisonReportDTO,
    ComparisonReportResult,
)


def get_comparison_report_data(
    db: Session,
    comparison_id: int,
) -> Optional[dict]:
    """
    Fetch all stored data required to generate a comparison report.

    This function only reads existing Comparison, Analysis,
    Benchmark, and ProgrammingLanguage records.

    It does NOT:
    - execute benchmarks
    - generate new workloads
    - create Analysis records
    - modify Comparison records
    - calculate Energy Saved
    - create rankings
    """

    # ---------------------------------------------------------
    # 1. Fetch comparison
    # ---------------------------------------------------------

    comparison = (
        db.query(Comparison)
        .filter(
            Comparison.comparison_id == comparison_id
        )
        .first()
    )

    if comparison is None:
        return None

    # ---------------------------------------------------------
    # 2. Fetch benchmark metadata
    # ---------------------------------------------------------

    benchmark = None

    if comparison.bench_id is not None:
        benchmark = (
            db.query(Benchmark)
            .filter(
                Benchmark.bench_id == comparison.bench_id
            )
            .first()
        )

    # ---------------------------------------------------------
    # 3. Fetch all analysis results belonging to comparison
    # ---------------------------------------------------------

    rows = (
        db.query(
            Analysis,
            ProgrammingLanguage,
        )
        .join(
            ProgrammingLanguage,
            Analysis.lang_id == ProgrammingLanguage.lang_id,
        )
        .filter(
            Analysis.comparison_id == comparison_id
        )
        .order_by(
            Analysis.analysis_id.asc()
        )
        .all()
    )

    # ---------------------------------------------------------
    # 4. Convert analysis rows into report-friendly data
    # ---------------------------------------------------------

    results = []

    for analysis, language in rows:
        results.append(
            ComparisonReportResult(
                analysis_id=analysis.analysis_id,
                language=language.lang_name,
                compiler=language.compiler,
                version=language.version,
                execution_time=analysis.execution_time,
                cpu_usage=analysis.cpu_usage,
                memory_usage=analysis.memory_usage,
                energy_consumption=analysis.energy_consumption,
                green_score=analysis.green_score,
                green_score_label=analysis.green_score_label,
                output_verified=analysis.output_verified,
                created_at=analysis.created_at,
                input_size=analysis.input_size,
                bench_size=analysis.bench_size,
                workload_type=analysis.workload_type,
            )
        )

    # ---------------------------------------------------------
    # 5. Resolve benchmark name
    # ---------------------------------------------------------

    benchmark_name = (
        benchmark.bench_name
        if benchmark is not None
        else (
            comparison.custom_benchmark_name
            or "Comparison"
        )
    )

    # ---------------------------------------------------------
    # 6. Resolve category
    # ---------------------------------------------------------

    category = (
        benchmark.category
        if benchmark is not None
        else comparison.custom_category
    )

    # ---------------------------------------------------------
    # 7. Return complete comparison report data
    # ---------------------------------------------------------

    return ComparisonReportDTO(
        comparison_id=comparison.comparison_id,
        user_id=comparison.user_id,
        comparison_type=comparison.comparison_type,
        benchmark_name=benchmark_name,
        category=category,
        bench_size=comparison.bench_size,
        input_size=comparison.input_size,
        workload_type=comparison.workload_type,
        created_at=comparison.created_at,
        results=results,
    )