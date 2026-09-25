from typing import Optional

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.benchmark import Benchmark
from app.models.programming_language import ProgrammingLanguage
from app.schemas.report import (
    ReportDTO,
    ReportMetadata,
    ReportMetrics,
)


def _get_benchmark_name(
    analysis: Analysis,
    benchmark: Optional[Benchmark],
) -> str:

    if analysis.analysis_type == "custom":
        return (
            analysis.custom_benchmark_name
            or "Custom Benchmark"
        )

    if benchmark is not None:
        return benchmark.bench_name

    return "Unknown Benchmark"


def _get_category(
    analysis: Analysis,
    benchmark: Optional[Benchmark],
) -> Optional[str]:

    if analysis.analysis_type == "custom":
        return analysis.custom_category

    if benchmark is None:
        return None

    for field_name in (
        "category",
        "bench_category",
        "benchmark_category",
    ):
        value = getattr(
            benchmark,
            field_name,
            None,
        )

        if value:
            return value

    return None

def _get_runtime(
    analysis: Analysis,
    language: ProgrammingLanguage,
) -> Optional[str]:

    metadata = analysis.benchmark_metadata

    if isinstance(metadata, dict):
        for key in (
            "runtime",
            "runtime_version",
            "execution_runtime",
        ):
            value = metadata.get(key)

            if value:
                return str(value)

    # Fallback to programming_language table
    if language.version:
        return str(language.version)

    return None


def _get_compiler(
    analysis: Analysis,
    language: ProgrammingLanguage,
) -> Optional[str]:

    metadata = analysis.benchmark_metadata

    if isinstance(metadata, dict):
        for key in (
            "compiler",
            "compiler_version",
            "compiler_name",
        ):
            value = metadata.get(key)

            if value:
                return str(value)

    # Fallback to programming_language table
    if language.compiler:
        return str(language.compiler)

    return None

def _build_report_title(
    analysis: Analysis,
    benchmark: Optional[Benchmark],
    language: ProgrammingLanguage,
) -> str:

    benchmark_name = _get_benchmark_name(
        analysis,
        benchmark,
    )

    return (
        f"{benchmark_name} - "
        f"{language.lang_name} Performance Report"
    )


def _build_report_dto(
    analysis: Analysis,
    benchmark: Optional[Benchmark],
    language: ProgrammingLanguage,
) -> ReportDTO:

    benchmark_name = _get_benchmark_name(
        analysis,
        benchmark,
    )

    category = _get_category(
        analysis,
        benchmark,
    )

    metadata = ReportMetadata(
        benchmark_task=benchmark_name,
        category=category,
        analysis_type=analysis.analysis_type,
        language=language.lang_name,
        input_size=analysis.input_size,
        bench_size=analysis.bench_size,
        workload_type=analysis.workload_type,
        execution_date=analysis.created_at,
        runtime=_get_runtime(
            analysis,
            language,
        ),
        compiler=_get_compiler(
            analysis,
            language,
        ),
    )

    metrics = ReportMetrics(
        execution_time=analysis.execution_time,
        cpu_usage=analysis.cpu_usage,
        memory_usage=analysis.memory_usage,
        energy_consumption=analysis.energy_consumption,
        green_score=analysis.green_score,
        green_score_label=analysis.green_score_label,
        output_verified=analysis.output_verified,
    )

    return ReportDTO(
        report_title=_build_report_title(
            analysis,
            benchmark,
            language,
        ),
        analysis_id=analysis.analysis_id,
        user_id=analysis.user_id,
        metadata=metadata,
        metrics=metrics,
    )


def get_report_data(
    db: Session,
    analysis_id: int,
) -> Optional[ReportDTO]:

    row = (
        db.query(
            Analysis,
            Benchmark,
            ProgrammingLanguage,
        )
        .outerjoin(
            Benchmark,
            Analysis.bench_id
            == Benchmark.bench_id,
        )
        .join(
            ProgrammingLanguage,
            Analysis.lang_id
            == ProgrammingLanguage.lang_id,
        )
        .filter(
            Analysis.analysis_id
            == analysis_id
        )
        .first()
    )

    if row is None:
        return None

    analysis, benchmark, language = row

    return _build_report_dto(
        analysis=analysis,
        benchmark=benchmark,
        language=language,
    )