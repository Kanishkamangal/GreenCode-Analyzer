from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.benchmark import Benchmark
from app.models.programming_language import ProgrammingLanguage


def _get_benchmark_name(analysis, benchmark):
    """
    Resolve the user-facing benchmark name.

    Predefined analysis:
        Benchmark.bench_name

    Custom analysis:
        Analysis.custom_benchmark_name
    """

    if analysis.analysis_type == "custom":
        return (
            analysis.custom_benchmark_name
            or "Custom Benchmark"
        )

    if benchmark is not None:
        return benchmark.bench_name

    return "Unknown Benchmark"


def _get_category(analysis, benchmark):
    """
    Resolve category without assuming that every historical
    record has the same metadata shape.
    """

    if analysis.analysis_type == "custom":
        return analysis.custom_category

    if benchmark is None:
        return None

    # Support the existing benchmark schema without making
    # the history layer dependent on one particular category
    # column name.
    for field_name in (
        "category",
        "bench_category",
        "benchmark_category",
    ):
        value = getattr(benchmark, field_name, None)

        if value:
            return value

    return None


def _to_history_item(
    analysis,
    benchmark,
    language,
):
    return {
        "analysis_id": analysis.analysis_id,
        "user_id": analysis.user_id,
        "analysis_type": analysis.analysis_type,

        "benchmark_name": _get_benchmark_name(
            analysis,
            benchmark,
        ),

        "category": _get_category(
            analysis,
            benchmark,
        ),

        "language": language.lang_name,

        "bench_size": analysis.bench_size,
        "comparison_id": analysis.comparison_id,
        "input_size": analysis.input_size,
        "workload_type": analysis.workload_type,

        "execution_time": analysis.execution_time,
        "cpu_usage": analysis.cpu_usage,
        "memory_usage": analysis.memory_usage,
        "energy_consumption": analysis.energy_consumption,

        "green_score": analysis.green_score,
        "green_score_label": analysis.green_score_label,

        "output_verified": analysis.output_verified,
        "created_at": analysis.created_at,
    }


def get_history_by_user(
    db: Session,
    user_id: int,
):
    rows = (
        db.query(
            Analysis,
            Benchmark,
            ProgrammingLanguage,
        )
        .outerjoin(
            Benchmark,
            Analysis.bench_id == Benchmark.bench_id,
        )
        .join(
            ProgrammingLanguage,
            Analysis.lang_id
            == ProgrammingLanguage.lang_id,
        )
        .filter(
            Analysis.user_id == user_id
        )
        .order_by(
            Analysis.created_at.desc(),
            Analysis.analysis_id.desc(),
        )
        .all()
    )

    items = [
        _to_history_item(
            analysis=analysis,
            benchmark=benchmark,
            language=language,
        )
        for analysis, benchmark, language in rows
    ]

    return {
        "items": items,
        "total": len(items),
    }


def get_history_item(
    db: Session,
    analysis_id: int,
):
    row = (
        db.query(
            Analysis,
            Benchmark,
            ProgrammingLanguage,
        )
        .outerjoin(
            Benchmark,
            Analysis.bench_id == Benchmark.bench_id,
        )
        .join(
            ProgrammingLanguage,
            Analysis.lang_id
            == ProgrammingLanguage.lang_id,
        )
        .filter(
            Analysis.analysis_id == analysis_id
        )
        .first()
    )

    if row is None:
        return None

    analysis, benchmark, language = row

    return _to_history_item(
        analysis=analysis,
        benchmark=benchmark,
        language=language,
    )