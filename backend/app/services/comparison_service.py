from typing import Optional

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.benchmark import Benchmark
from app.models.comparison import Comparison
from app.models.programming_language import ProgrammingLanguage


def get_comparison(
    db: Session,
    comparison_id: int,
):
    comparison = (
        db.query(Comparison)
        .filter(
            Comparison.comparison_id
            == comparison_id
        )
        .first()
    )

    if comparison is None:
        return None

    rows = (
        db.query(
            Analysis,
            ProgrammingLanguage,
        )
        .join(
            ProgrammingLanguage,
            Analysis.lang_id
            == ProgrammingLanguage.lang_id,
        )
        .filter(
            Analysis.comparison_id
            == comparison_id
        )
        .order_by(
            Analysis.analysis_id.asc()
        )
        .all()
    )

    benchmark = None

    if comparison.bench_id is not None:
        benchmark = (
            db.query(Benchmark)
            .filter(
                Benchmark.bench_id
                == comparison.bench_id
            )
            .first()
        )

    return {
        "comparison": comparison,
        "benchmark": benchmark,
        "results": [
            {
                "analysis": analysis,
                "language": language,
            }
            for analysis, language in rows
        ],
    }


def get_comparisons_by_user(
    db: Session,
    user_id: int,
):
    comparisons = (
        db.query(Comparison)
        .filter(
            Comparison.user_id == user_id
        )
        .order_by(
            Comparison.created_at.desc(),
            Comparison.comparison_id.desc(),
        )
        .all()
    )

    results = []

    for comparison in comparisons:
        benchmark = None

        if comparison.bench_id is not None:
            benchmark = (
                db.query(Benchmark)
                .filter(
                    Benchmark.bench_id
                    == comparison.bench_id
                )
                .first()
            )

        analysis_rows = (
            db.query(
                Analysis,
                ProgrammingLanguage,
            )
            .join(
                ProgrammingLanguage,
                Analysis.lang_id
                == ProgrammingLanguage.lang_id,
            )
            .filter(
                Analysis.comparison_id
                == comparison.comparison_id
            )
            .order_by(
                Analysis.analysis_id.asc()
            )
            .all()
        )

        results.append(
            {
                "comparison": comparison,
                "benchmark": benchmark,
                "results": [
                    {
                        "analysis": analysis,
                        "language": language,
                    }
                    for analysis, language in analysis_rows
                ],
            }
        )

    return {
        "items": results,
        "total": len(results),
    }