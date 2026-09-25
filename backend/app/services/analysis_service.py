from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate

def create_analysis(
    db: Session,
    analysis: AnalysisCreate,
    execution_time: float,
    cpu_usage: float,
    memory_usage: float,
    energy_consumption: float | None,
    green_score: float | None = None,
    green_score_label: str | None = None,
    output_verified: bool | None = True
):

    new_analysis = Analysis(
    comparison_id=analysis.comparison_id,
    user_id=analysis.user_id,

    analysis_type=analysis.analysis_type,

    bench_id=analysis.bench_id,
    lang_id=analysis.lang_id,
    bench_size=analysis.bench_size,

    custom_category=analysis.custom_category,
    custom_benchmark_name=(
        analysis.custom_benchmark_name
    ),
    custom_description=(
        analysis.custom_description
    ),
    benchmark_metadata=(
        analysis.benchmark_metadata
    ),
    workload_type=analysis.workload_type,
    input_size=analysis.input_size,

    execution_time=execution_time,
    cpu_usage=cpu_usage,
    memory_usage=memory_usage,
    energy_consumption=energy_consumption,

    green_score=green_score,
    green_score_label=green_score_label,

    output_verified=output_verified
)

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis


def get_analysis_by_id(db: Session, analysis_id: int):
    return db.query(Analysis).filter(
        Analysis.analysis_id == analysis_id
    ).first()


def get_all_analyses(db: Session):
    return db.query(Analysis).all()


def get_analysis_by_user(db: Session, user_id: int):
    return db.query(Analysis).filter(
        Analysis.user_id == user_id
    ).all()


def delete_analysis(db: Session, analysis_id: int):

    analysis = get_analysis_by_id(db, analysis_id)

    if not analysis:
        return None

    db.delete(analysis)
    db.commit()

    return analysis