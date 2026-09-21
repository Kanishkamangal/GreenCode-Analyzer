from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import uuid
import threading
from datetime import datetime
from app.database.database import (
    get_db,
    SessionLocal,
)
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisComparisonCreate,
    CustomAnalysisComparisonCreate,
    ReferenceCodeAnalysisRequest,
    AnalysisResponse,
)
from app.services import analysis_service
from app.models.benchmark import Benchmark
from app.models.comparison import Comparison
from app.models.programming_language import ProgrammingLanguage
from app.services.benchmark_engine import run_benchmark
from app.services.custom_benchmark_engine import (
    run_custom_benchmark,
)
from app.services.green_score_service import (
    calculate_green_scores,
)
from app.services.reference_code_analyzer import (
    analyze_reference_code,
)
from app.services.input_contract_analyzer import (
    detect_input_contract,
)
from app.services.workload_resolver import (
    resolve_benchmark_workload,
)
from app.services.custom_workload_generator import (
    get_input_generation_capability,
)
logger = logging.getLogger(__name__)
CUSTOM_ANALYSIS_JOBS = {}
CUSTOM_ANALYSIS_JOBS_LOCK = threading.Lock()
REFERENCE_ANALYSIS_JOBS = {}
REFERENCE_ANALYSIS_JOBS_LOCK = threading.Lock()
PREDEFINED_ANALYSIS_JOBS = {}
PREDEFINED_ANALYSIS_JOBS_LOCK = threading.Lock()
router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

# -----------------------------------
# Validate Custom Input Mode
# -----------------------------------

def validate_custom_input_mode(
    comparison,
    reference_language_name: str,
):
    input_contract = detect_input_contract(
        reference_code=comparison.reference_code,
        language=reference_language_name,
    )

    resolved_workload = resolve_benchmark_workload(
        benchmark_name=comparison.custom_benchmark_name,
        description=comparison.custom_description,
        reference_code=comparison.reference_code,
        workload_type=comparison.workload_type,
        input_contract=input_contract,
    )

    generation_mode = resolved_workload.get(
        "generation_mode",
        "custom",
    )

    can_generate = bool(
        resolved_workload.get(
            "can_generate",
            False,
        )
    )

    has_custom_input = bool(
        comparison.custom_input
        and comparison.custom_input.strip()
    )

    contract_type = (
        str(
            input_contract.get("contract_type")
            or ""
        )
        .strip()
        .lower()
    )

    if generation_mode == "blocked":
        raise HTTPException(
            status_code=400,
            detail=(
                resolved_workload.get("reason")
                or "Benchmark workload resolution is blocked."
            ),
        )

    if contract_type == "no-input":
        return input_contract, resolved_workload

    if can_generate:
        if (
            comparison.input_size is None
            or comparison.input_size <= 0
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Input size must be greater than zero "
                    "for automatic workload generation."
                ),
            )

        return input_contract, resolved_workload

    if not has_custom_input:
        raise HTTPException(
            status_code=400,
            detail=(
                resolved_workload.get("reason")
                or (
                    "Automatic workload generation is not "
                    "supported for this input contract. "
                    "Please provide Custom Input."
                )
            ),
        )

    return input_contract, resolved_workload

def update_predefined_job(
    job_id: str,
    step: str,
    status: str,
    message: str,
):
    with PREDEFINED_ANALYSIS_JOBS_LOCK:
        job = PREDEFINED_ANALYSIS_JOBS.get(job_id)

        if job is None:
            return

        job["current_step"] = step

        if "steps" not in job:
            job["steps"] = {}

        job["steps"][step] = {
            "status": status,
            "message": message,
        }

        job["updated_at"] = datetime.utcnow().isoformat()


def mark_predefined_job_failed(
    job_id: str,
    message: str,
):
    with PREDEFINED_ANALYSIS_JOBS_LOCK:
        job = PREDEFINED_ANALYSIS_JOBS.get(job_id)

        if job is None:
            return

        job["status"] = "failed"
        job["current_step"] = None
        job["error"] = message
        job["updated_at"] = datetime.utcnow().isoformat()


def mark_predefined_job_completed(
    job_id: str,
    results,
    comparison_id=None,
):
    with PREDEFINED_ANALYSIS_JOBS_LOCK:
        job = PREDEFINED_ANALYSIS_JOBS.get(job_id)

        if job is None:
            return

        job["status"] = "completed"
        job["current_step"] = None
        job["results"] = results
        job["comparison_id"] = comparison_id
        job["updated_at"] = datetime.utcnow().isoformat()

def update_custom_job(
    job_id: str,
    step: str,
    status: str,
    message: str,
):

    with CUSTOM_ANALYSIS_JOBS_LOCK:

        job = CUSTOM_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["current_step"] = step
        if "steps" not in job:
            job["steps"] = {}
        job["steps"][step] = {
            "status": status,
            "message": message,
        }

        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )

def mark_custom_job_failed(
    job_id: str,
    message: str,
):

    with CUSTOM_ANALYSIS_JOBS_LOCK:

        job = CUSTOM_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["status"] = "failed"
        job["error"] = message
        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )

def mark_custom_job_completed(
    job_id: str,
    results,
    benchmark_metadata=None,
    comparison_id=None,
):

    with CUSTOM_ANALYSIS_JOBS_LOCK:

        job = CUSTOM_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["status"] = "completed"
        job["current_step"] = None
        job["results"] = results
        job["comparison_id"] = comparison_id
        job["benchmark_metadata"] = benchmark_metadata
        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )


def update_reference_job(
    job_id: str,
    step: str,
    status: str,
    message: str,
):

    with REFERENCE_ANALYSIS_JOBS_LOCK:

        job = REFERENCE_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["current_step"] = step

        if "steps" not in job:
            job["steps"] = {}

        job["steps"][step] = {
            "status": status,
            "message": message,
        }

        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )


def mark_reference_job_failed(
    job_id: str,
    message: str,
):

    with REFERENCE_ANALYSIS_JOBS_LOCK:

        job = REFERENCE_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["status"] = "failed"
        job["current_step"] = None
        job["error"] = message
        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )


def mark_reference_job_completed(
    job_id: str,
    result: dict,
):

    with REFERENCE_ANALYSIS_JOBS_LOCK:

        job = REFERENCE_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            return

        job["status"] = "completed"
        job["current_step"] = None
        job["result"] = result
        job["updated_at"] = (
            datetime.utcnow().isoformat()
        )

def run_reference_analysis_job(
    job_id: str,
    reference_code: str,
):

    try:

        with REFERENCE_ANALYSIS_JOBS_LOCK:

            job = REFERENCE_ANALYSIS_JOBS.get(
                job_id
            )

            if job is not None:
                job["status"] = "running"
                job["updated_at"] = (
                    datetime.utcnow().isoformat()
                )

        # -----------------------------------
        # 1. Language + syntax analysis
        # -----------------------------------

        update_reference_job(
            job_id=job_id,
            step="language",
            status="processing",
            message="Detecting programming language",
        )

        reference_analysis = (
            analyze_reference_code(
                reference_code
            )
        )

        language = reference_analysis.get(
            "language"
        )

        if language is None:

            update_reference_job(
                job_id=job_id,
                step="language",
                status="failed",
                message=(
                    "Programming language "
                    "could not be detected"
                ),
            )

            raise ValueError(
                "Programming language could not "
                "be detected reliably."
            )

        update_reference_job(
            job_id=job_id,
            step="language",
            status="completed",
            message=f"Detected {language}",
        )

        # -----------------------------------
        # 2. Syntax result
        # -----------------------------------

        update_reference_job(
            job_id=job_id,
            step="syntax",
            status="processing",
            message="Validating syntax",
        )

        syntax_valid = (
            reference_analysis.get(
                "syntax_valid",
                False,
            )
        )

        if not syntax_valid:

            update_reference_job(
                job_id=job_id,
                step="syntax",
                status="failed",
                message="Syntax validation failed",
            )

            result = {
                "detected_language": {
                    "name": language,
                    "confidence": (
                        reference_analysis.get(
                            "confidence",
                            0.0,
                        )
                    ),
                    "reason": (
                        reference_analysis.get(
                            "reason"
                        )
                    ),
                },
                "syntax_validation": {
                    "valid": False,
                    "errors": (
                        reference_analysis.get(
                            "syntax_errors",
                            [],
                        )
                    ),
                },
                "input_contract": None,
                "workload_resolution": None,
            }

            mark_reference_job_completed(
                job_id=job_id,
                result=result,
            )

            return

        update_reference_job(
            job_id=job_id,
            step="syntax",
            status="completed",
            message="Syntax validation passed",
        )

        # -----------------------------------
        # 3. Input contract
        # -----------------------------------

        update_reference_job(
            job_id=job_id,
            step="input-contract",
            status="processing",
            message="Detecting input contract",
        )

        input_contract = (
            detect_input_contract(
                reference_code=reference_code,
                language=language,
            )
        )

        workload_resolution = resolve_benchmark_workload(
            benchmark_name=None,
            description=None,
            reference_code=reference_code,
            workload_type=None,
            input_contract=input_contract,
        )

        update_reference_job(
            job_id=job_id,
            step="input-contract",
            status="completed",
            message="Input contract detected",
        )

        # -----------------------------------
        # Final result
        # -----------------------------------

        result = {
            "detected_language": {
                "name": language,
                "confidence": (
                    reference_analysis.get(
                        "confidence",
                        0.0,
                    )
                ),
                "reason": (
                    reference_analysis.get(
                        "reason"
                    )
                ),
            },

            "syntax_validation": {
                "valid": True,
                "errors": [],
            },

            "input_contract":
                input_contract,

            "workload_resolution":
                workload_resolution,
            "benchmark_metadata": workload_resolution.get(
                "benchmark_metadata"
            ),
        }

        mark_reference_job_completed(
            job_id=job_id,
            result=result,
        )

    except Exception as exc:

        logger.exception(
            "Reference analysis job failed. "
            "Job ID: %s",
            job_id,
        )

        mark_reference_job_failed(
            job_id=job_id,
            message=str(exc),
        )

def run_predefined_analysis_job(
    job_id: str,
    comparison_data: dict,
):
    db = SessionLocal()

    try:
        with PREDEFINED_ANALYSIS_JOBS_LOCK:
            job = PREDEFINED_ANALYSIS_JOBS.get(job_id)

            if job is not None:
                job["status"] = "running"
                job["updated_at"] = datetime.utcnow().isoformat()

        benchmark = (
            db.query(Benchmark)
            .filter(
                Benchmark.bench_id
                == comparison_data["bench_id"]
            )
            .first()
        )

        if benchmark is None:
            raise ValueError("Benchmark not found.")

        lang_ids = list(
            dict.fromkeys(
                comparison_data["lang_ids"]
            )
        )

        if not lang_ids:
            raise ValueError(
                "Select at least one programming language."
            )

        raw_results = []

        for lang_id in lang_ids:
            language = (
                db.query(ProgrammingLanguage)
                .filter(
                    ProgrammingLanguage.lang_id
                    == lang_id
                )
                .first()
            )

            if language is None:
                raise ValueError(
                    f"Programming language {lang_id} not found."
                )

            language_step_prefix = str(lang_id)

            def progress_callback(
                event,
                prefix=language_step_prefix,
                language_name=language.lang_name,
            ):
                engine_step = event["step"]

                if engine_step == "workload":
                    step_id = "workload"
                else:
                    step_id = (
                        f"{prefix}-{engine_step}"
                    )

                update_predefined_job(
                    job_id=job_id,
                    step=step_id,
                    status=event["status"],
                    message=event["message"],
                )

            result = run_benchmark(
                benchmark_name=benchmark.bench_name,
                folder_name=benchmark.folder_name,
                language=language.lang_name,
                bench_size=comparison_data[
                    "bench_size"
                ],
                progress_callback=progress_callback,
            )

            raw_results.append({
                "lang_id": lang_id,
                "execution_time":
                    result["execution_time"],
                "cpu_usage":
                    result["cpu_usage"],
                "memory_usage":
                    result["memory_usage"],
                "energy_consumption":
                    result["energy_consumption"],
                "output_verified":
                    result["output_verified"],
                "input_size":
                    result["input_size"],
            })

        update_predefined_job(
            job_id=job_id,
            step="green-score",
            status="processing",
            message="Calculating Green Scores",
        )

        scored_results = calculate_green_scores(
            raw_results
        )
        # -----------------------------------
        # Create Comparison Record
        # -----------------------------------

        comparison_record = Comparison(
            user_id=comparison_data["user_id"],
            bench_id=comparison_data["bench_id"],
            comparison_type="predefined",
            bench_size=comparison_data["bench_size"],
        )

        db.add(comparison_record)
        db.commit()
        db.refresh(comparison_record)

        # -----------------------------------
        # Save Analysis Results
        # -----------------------------------

        update_predefined_job(
            job_id=job_id,
            step="green-score",
            status="completed",
            message="Green Scores calculated",
        )

        update_predefined_job(
            job_id=job_id,
            step="save",
            status="processing",
            message="Saving analysis results",
        )

        response_results = []

        for result in scored_results:
            analysis_data = AnalysisCreate(
                user_id=comparison_data["user_id"],
                comparison_id=(
                    comparison_record.comparison_id
                ),
                bench_id=comparison_data["bench_id"],
                lang_id=result["lang_id"],
                analysis_type="predefined",
                bench_size=comparison_data[
                    "bench_size"
                ],
                workload_type=None,
                input_size=result.get(
                    "input_size"
                ),
            )

            saved_analysis = (
                analysis_service.create_analysis(
                    db=db,
                    analysis=analysis_data,
                    execution_time=result[
                        "execution_time"
                    ],
                    cpu_usage=result[
                        "cpu_usage"
                    ],
                    memory_usage=result[
                        "memory_usage"
                    ],
                    energy_consumption=result[
                        "energy_consumption"
                    ],
                    green_score=result.get(
                        "green_score"
                    ),
                    green_score_label=result.get(
                        "green_score_label"
                    ),
                    output_verified=result[
                        "output_verified"
                    ],
                )
            )

            response_results.append(
                AnalysisResponse.model_validate(
                    saved_analysis
                ).model_dump(
                    mode="json"
                )
            )

        update_predefined_job(
            job_id=job_id,
            step="save",
            status="completed",
            message="Analysis results saved",
        )

        mark_predefined_job_completed(
            job_id=job_id,
            results=response_results,
            comparison_id=(
                comparison_record.comparison_id
            ),
        )

    except Exception as exc:
        logger.exception(
            "Predefined benchmark job failed. "
            "Job ID: %s",
            job_id,
        )

        db.rollback()

        mark_predefined_job_failed(
            job_id=job_id,
            message=str(exc),
        )

    finally:
        db.close()

def run_custom_analysis_job(
    job_id: str,
    comparison_data: dict,
):

    db = SessionLocal()

    try:

        with CUSTOM_ANALYSIS_JOBS_LOCK:

            job = CUSTOM_ANALYSIS_JOBS.get(
                job_id
            )

            if job is not None:
                job["status"] = "running"

        # -----------------------------------
        # Reference language
        # -----------------------------------

        reference_language = (
            db.query(ProgrammingLanguage)
            .filter(
                ProgrammingLanguage.lang_id
                ==
                comparison_data[
                    "reference_lang_id"
                ]
            )
            .first()
        )

        if reference_language is None:
            raise ValueError(
                "Reference programming language "
                "not found."
            )
        
        # -----------------------------------
        # Exact input contract
        # -----------------------------------

        input_contract = detect_input_contract(
            reference_code=comparison_data[
                "reference_code"
            ],
            language=reference_language.lang_name,
        )

        # -----------------------------------
        # Target languages
        # -----------------------------------

        target_ids = list(
            dict.fromkeys(
                comparison_data[
                    "target_lang_ids"
                ]
            )
        )

        target_languages = []

        for lang_id in target_ids:

            if (
                lang_id
                ==
                comparison_data[
                    "reference_lang_id"
                ]
            ):
                continue

            language = (
                db.query(
                    ProgrammingLanguage
                )
                .filter(
                    ProgrammingLanguage.lang_id
                    == lang_id
                )
                .first()
            )

            if language is None:
                raise ValueError(
                    f"Programming language "
                    f"{lang_id} not found."
                )

            target_languages.append(
                language.lang_name
            )

        if not target_languages:
            raise ValueError(
                "Select at least one target language."
            )

        # -----------------------------------
        # Real progress callback
        # -----------------------------------

        def progress_callback(event):

            update_custom_job(
                job_id=job_id,
                step=event["step"],
                status=event["status"],
                message=event["message"],
            )

        # -----------------------------------
        # Run benchmark
        # -----------------------------------

        benchmark_result = run_custom_benchmark(
            benchmark_name=(
                comparison_data[
                    "custom_benchmark_name"
                ]
            ),

            benchmark_category=(
                comparison_data[
                    "custom_category"
                ]
            ),

            description=(
                comparison_data.get(
                    "custom_description"
                )
            ),

            workload_type=(
                comparison_data.get(
                    "workload_type"
                )
            ),

            input_size=(
                comparison_data.get(
                    "input_size"
                )
            ),

            custom_input=(
                comparison_data.get(
                    "custom_input"
                )
            ),

            reference_language=(
                reference_language.lang_name
            ),

            reference_code=(
                comparison_data[
                    "reference_code"
                ]
            ),

            target_languages=(
                target_languages
            ),

            progress_callback=(
                progress_callback
            ),
            input_contract=input_contract,
        )
        benchmark_metadata = benchmark_result.get(
            "benchmark_metadata"
        )

        resolved_benchmark_name = benchmark_result.get(
            "benchmark_name"
        )

        resolved_benchmark_category = benchmark_result.get(
            "benchmark_category"
        )

        resolved_description = benchmark_result.get(
            "description"
        )

        results = benchmark_result.get(
            "results",
            []
        )
        # -----------------------------------
        # Convert language names -> IDs
        # -----------------------------------

        raw_results = []
        skipped_results = []

        for result in results:

            result_status = result.get(
                "status",
                "success",
            )

            if result_status != "success":
                skipped_results.append({
                    "language": result.get("language"),
                    "status": result_status,
                    "reason": result.get(
                        "reason",
                        "Implementation did not complete successfully.",
                    ),
                })
                continue

            language_name = result.get("language")

            if not language_name:
                skipped_results.append({
                    "language": None,
                    "status": "failed",
                    "reason": "Benchmark result did not include a language.",
                })
                continue

            language = (
                db.query(
                    ProgrammingLanguage
                )
                .filter(
                    ProgrammingLanguage.lang_name
                    == language_name
                )
                .first()
            )

            if language is None:
                raise ValueError(
                    "Programming language "
                    f"{language_name} "
                    "not found."
                )

            execution_time = result.get(
                "execution_time"
            )
            cpu_usage = result.get(
                "cpu_usage"
            )
            memory_usage = result.get(
                "memory_usage"
            )
            energy_consumption = result.get(
                "energy_consumption"
            )
            output_verified = result.get(
                "output_verified",
                False,
            )

            missing_metrics = []

            if execution_time is None:
                missing_metrics.append(
                    "execution_time"
                )

            if cpu_usage is None:
                missing_metrics.append(
                    "cpu_usage"
                )

            if memory_usage is None:
                missing_metrics.append(
                    "memory_usage"
                )

            if energy_consumption is None:
                missing_metrics.append(
                    "energy_consumption"
                )

            if missing_metrics:
                skipped_results.append({
                    "language": language_name,
                    "status": "failed",
                    "reason": (
                        "Missing benchmark metrics: "
                        + ", ".join(missing_metrics)
                    ),
                })
                continue

            raw_results.append({
                "lang_id":
                    language.lang_id,

                "execution_time":
                    execution_time,

                "cpu_usage":
                    cpu_usage,

                "memory_usage":
                    memory_usage,

                "energy_consumption":
                    energy_consumption,

                "output_verified":
                    output_verified,
            })

        if not raw_results:
            raise ValueError(
                "No implementation completed successfully, "
                "so no benchmark measurements are available."
            )

        # -----------------------------------
        # Green Score
        # -----------------------------------

        update_custom_job(
            job_id=job_id,
            step="green-score",
            status="processing",
            message="Calculating Green Scores",
        )

        scored_results = (
            calculate_green_scores(
                raw_results
            )
        )
        # -----------------------------------
        # Create Comparison Record
        # -----------------------------------

        comparison_record = Comparison(
            user_id=comparison_data["user_id"],
            comparison_type="custom",
            bench_id=None,
            bench_size=None,
            custom_category=resolved_benchmark_category,
            custom_benchmark_name=resolved_benchmark_name,
            workload_type=(
                comparison_data.get("workload_type")
                or benchmark_result.get("workload_type")
            ),
            input_size=comparison_data.get("input_size"),
        )

        db.add(comparison_record)
        db.commit()
        db.refresh(comparison_record)

        update_custom_job(
            job_id=job_id,
            step="green-score",
            status="completed",
            message="Green Scores calculated",
        )

        # -----------------------------------
        # Save results
        # -----------------------------------

        update_custom_job(
            job_id=job_id,
            step="save",
            status="processing",
            message="Saving analysis results",
        )

        response_results = []

        for result in scored_results:

            analysis_data = AnalysisCreate(
                user_id=(
                    comparison_data[
                        "user_id"
                    ]
                ),comparison_id=(
                    comparison_record.comparison_id
                ),

                analysis_type="custom",

                bench_id=None,

                lang_id=result["lang_id"],

                bench_size=None,

                custom_category=(
                    resolved_benchmark_category
                ),

                custom_benchmark_name=(
                    resolved_benchmark_name
                ),

                custom_description=(
                    resolved_description
                ),
                benchmark_metadata=benchmark_metadata,
                workload_type=(
                    comparison_data.get(
                        "workload_type"
                    )
                    or benchmark_result.get(
                        "workload_type"
                    )
                ),
                input_size=(
                    comparison_data[
                        "input_size"
                    ]
                ),
            )

            saved_analysis = (
                analysis_service.create_analysis(
                    db=db,
                    analysis=analysis_data,

                    execution_time=(
                        result[
                            "execution_time"
                        ]
                    ),

                    cpu_usage=(
                        result[
                            "cpu_usage"
                        ]
                    ),

                    memory_usage=(
                        result[
                            "memory_usage"
                        ]
                    ),

                    energy_consumption=(
                        result[
                            "energy_consumption"
                        ]
                    ),

                    green_score=(
                        result.get(
                            "green_score"
                        )
                    ),

                    green_score_label=(
                        result.get(
                            "green_score_label"
                        )
                    ),

                    output_verified=(
                        result[
                            "output_verified"
                        ]
                    ),
                )
            )

            # Store plain JSON-safe data,
            # not SQLAlchemy objects.
            response_results.append(
                AnalysisResponse.model_validate(
                    saved_analysis
                ).model_dump(
                    mode="json"
                )
            )

        update_custom_job(
            job_id=job_id,
            step="save",
            status="completed",
            message="Analysis results saved",
        )

        mark_custom_job_completed(
            job_id=job_id,
            results=response_results,
            benchmark_metadata=benchmark_metadata,
            comparison_id=(
                comparison_record.comparison_id
            ),
        )

    except Exception as exc:

        logger.exception(
            "Custom benchmark job failed. "
            "Job ID: %s",
            job_id,
        )

        mark_custom_job_failed(
            job_id=job_id,
            message=str(exc),
        )

    finally:

        db.close()

# -----------------------------------
# Create Analysis
# -----------------------------------
@router.post(
    "/",
    response_model=AnalysisResponse
)
def create_analysis(
    analysis: AnalysisCreate,
    db: Session = Depends(get_db)
):

    benchmark = db.query(Benchmark).filter(
        Benchmark.bench_id == analysis.bench_id
    ).first()

    if benchmark is None:
        raise HTTPException(
            status_code=404,
            detail="Benchmark not found."
        )


    language = db.query(ProgrammingLanguage).filter(
        ProgrammingLanguage.lang_id == analysis.lang_id
    ).first()

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Programming language not found."
        )


    try:

        result = run_benchmark(
            benchmark_name=benchmark.bench_name,
            folder_name=benchmark.folder_name,
            language=language.lang_name,
            bench_size=analysis.bench_size
        )

    except (
        ValueError,
        FileNotFoundError,
        RuntimeError,
        TimeoutError
    ) as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    execution_time = result["execution_time"]
    cpu_usage = result["cpu_usage"]
    memory_usage = result["memory_usage"]
    energy_consumption = result["energy_consumption"]
    output_verified = result["output_verified"]

    return analysis_service.create_analysis(
        db=db,
        analysis=analysis,
        execution_time=execution_time,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        energy_consumption=energy_consumption,
        output_verified=output_verified,
    )

# -----------------------------------
# Create Benchmark Comparison
# -----------------------------------
@router.post(
    "/comparison",
    response_model=list[AnalysisResponse]
)
def create_comparison(
    comparison: AnalysisComparisonCreate,
    db: Session = Depends(get_db)
):

    # At least one language must be selected
    if not comparison.lang_ids:
        raise HTTPException(
            status_code=400,
            detail="Select at least one programming language."
        )

    # Remove accidental duplicate language IDs
    lang_ids = list(
        dict.fromkeys(
            comparison.lang_ids
        )
    )

    # -----------------------------------
    # Find benchmark
    # -----------------------------------

    benchmark = db.query(Benchmark).filter(
        Benchmark.bench_id
        == comparison.bench_id
    ).first()

    if benchmark is None:
        raise HTTPException(
            status_code=404,
            detail="Benchmark not found."
        )

    # -----------------------------------
    # Run every selected language
    # -----------------------------------

    raw_results = []

    for lang_id in lang_ids:

        language = (
            db.query(ProgrammingLanguage)
            .filter(
                ProgrammingLanguage.lang_id
                == lang_id
            )
            .first()
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Programming language "
                    f"{lang_id} not found."
                )
            )

        try:

            result = run_benchmark(
                benchmark_name=benchmark.bench_name,
                folder_name=benchmark.folder_name,
                language=language.lang_name,
                bench_size=comparison.bench_size
            )

        except (
            ValueError,
            FileNotFoundError,
            RuntimeError,
            TimeoutError
        ) as e:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"{language.lang_name}: {str(e)}"
                )
            )

        raw_results.append({
            "lang_id": lang_id,

            "execution_time":
                result["execution_time"],

            "cpu_usage":
                result["cpu_usage"],

            "memory_usage":
                result["memory_usage"],

            "energy_consumption":
                result["energy_consumption"],

            "output_verified":
                result["output_verified"],
        })

    # -----------------------------------
    # Calculate comparative Green Scores
    # -----------------------------------

    scored_results = calculate_green_scores(
        raw_results
    )
    comparison_record = Comparison(
        user_id=comparison.user_id,
        bench_id=comparison.bench_id,
        comparison_type="predefined",
        bench_size=comparison.bench_size,
    )

    db.add(comparison_record)
    db.commit()
    db.refresh(comparison_record)
    # -----------------------------------
    # Save every result
    # -----------------------------------

    saved_results = []

    for result in scored_results:

        analysis_data = AnalysisCreate(
            user_id=comparison.user_id,
            bench_id=comparison.bench_id,
            comparison_id=(
                comparison_record.comparison_id
            ),
            lang_id=result["lang_id"],
            bench_size=comparison.bench_size
        )

        saved_analysis = (
            analysis_service.create_analysis(
                db=db,
                analysis=analysis_data,

                execution_time=
                    result["execution_time"],

                cpu_usage=
                    result["cpu_usage"],

                memory_usage=
                    result["memory_usage"],

                energy_consumption=
                    result["energy_consumption"],

                green_score=
                    result.get("green_score"),

                green_score_label=
                    result.get(
                        "green_score_label"
                    ),

                output_verified=
                    result["output_verified"],
            )
        )

        saved_results.append(
            saved_analysis
        )

    return saved_results

# -----------------------------------
# Start Predefined Benchmark Job
# -----------------------------------

@router.post(
    "/comparison/start"
)
def start_predefined_comparison(
    comparison: AnalysisComparisonCreate,
):
    if not comparison.lang_ids:
        raise HTTPException(
            status_code=400,
            detail=(
                "Select at least one "
                "programming language."
            ),
        )

    job_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    with PREDEFINED_ANALYSIS_JOBS_LOCK:
        PREDEFINED_ANALYSIS_JOBS[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "current_step": None,
            "steps": {},
            "results": None,
            "error": None,
            "created_at": now,
            "updated_at": now,
        }

    comparison_data = comparison.model_dump()

    worker = threading.Thread(
        target=run_predefined_analysis_job,
        args=(
            job_id,
            comparison_data,
        ),
        daemon=True,
    )

    worker.start()

    return {
        "job_id": job_id,
        "status": "queued",
    }


# -----------------------------------
# Get Predefined Benchmark Job Status
# -----------------------------------

@router.get(
    "/comparison/status/{job_id}"
)
def get_predefined_comparison_status(
    job_id: str,
):
    with PREDEFINED_ANALYSIS_JOBS_LOCK:
        job = PREDEFINED_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Predefined benchmark job "
                    "not found."
                ),
            )

        return {
            "job_id": job["job_id"],
            "status": job["status"],
            "current_step": job[
                "current_step"
            ],
            "steps": dict(
                job["steps"]
            ),
            "results": job["results"],
            "comparison_id": job.get(
                "comparison_id"
            ),
            "error": job["error"],
            "created_at": job["created_at"],
            "updated_at": job["updated_at"],
        }
    
# -----------------------------------
# Start Reference Analysis Job
# -----------------------------------

@router.post(
    "/custom-comparison/reference-analysis/start"
)
def start_reference_analysis(
    request: ReferenceCodeAnalysisRequest,
):

    reference_code = (
        request.reference_code.strip()
    )

    if not reference_code:
        raise HTTPException(
            status_code=400,
            detail=(
                "Reference code cannot be empty."
            ),
        )

    job_id = str(
        uuid.uuid4()
    )

    now = (
        datetime.utcnow().isoformat()
    )

    with REFERENCE_ANALYSIS_JOBS_LOCK:

        REFERENCE_ANALYSIS_JOBS[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "current_step": None,
            "steps": {},
            "result": None,
            "error": None,
            "created_at": now,
            "updated_at": now,
        }

    worker = threading.Thread(
        target=run_reference_analysis_job,
        args=(
            job_id,
            reference_code,
        ),
        daemon=True,
    )

    worker.start()

    return {
        "job_id": job_id,
        "status": "queued",
    }

# -----------------------------------
# Get Reference Analysis Job Status
# -----------------------------------

@router.get(
    "/custom-comparison/reference-analysis/status/{job_id}"
)
def get_reference_analysis_status(
    job_id: str,
):

    with REFERENCE_ANALYSIS_JOBS_LOCK:

        job = REFERENCE_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Reference analysis job "
                    "not found."
                ),
            )

        return {
            "job_id":
                job["job_id"],

            "status":
                job["status"],

            "current_step":
                job["current_step"],

            "steps":
                dict(job["steps"]),

            "result":
                job["result"],

            

            "error":
                job["error"],

            "created_at":
                job["created_at"],

            "updated_at":
                job["updated_at"],
        }


# -----------------------------------
# Analyze Reference Code
# -----------------------------------

@router.post(
    "/custom-comparison/analyze-reference"
)
def analyze_reference(
    request: ReferenceCodeAnalysisRequest,
):

    reference_code = request.reference_code.strip()

    if not reference_code:
        raise HTTPException(
            status_code=400,
            detail="Reference code cannot be empty."
        )

    # -----------------------------------
    # 1. Language + syntax analysis
    # -----------------------------------

    reference_analysis = (
        analyze_reference_code(
            reference_code
        )
    )

    language = reference_analysis.get(
        "language"
    )

    if language is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Programming language could not "
                "be detected reliably."
            ),
        )
    if not reference_analysis.get("syntax_valid", False):
        return {
            "detected_language": {
                "name": language,
                "confidence": reference_analysis.get(
                    "confidence",
                    0.0,
                ),
                "reason": reference_analysis.get(
                    "reason"
                ),
            },
            "syntax_validation": {
                "valid": False,
                "errors": reference_analysis.get(
                    "syntax_errors",
                    []
                ),
            },
            "input_contract": None,
            "workload_resolution": None,
        }

    # -----------------------------------
    # 2. Input contract
    # -----------------------------------

    input_contract = detect_input_contract(
        reference_code=reference_code,
        language=language,
    )

    workload_resolution = resolve_benchmark_workload(
        benchmark_name=None,
        description=None,
        reference_code=reference_code,
        workload_type=None,
        input_contract=input_contract,
    )

    # -----------------------------------
    # 3. Workload resolution
    # -----------------------------------

    return {
        "detected_language": {
            "name": language,
            "confidence": (
                reference_analysis.get(
                    "confidence",
                    0.0,
                )
            ),
            "reason": (
                reference_analysis.get(
                    "reason"
                )
            ),
        },

        "syntax_validation": {
            "valid": (
                reference_analysis.get(
                    "syntax_valid",
                    False,
                )
            ),
            "errors": (
                reference_analysis.get(
                    "syntax_errors",
                    []
                )
            ),
        },

        "input_contract": input_contract,

        "workload_resolution": workload_resolution,
        "benchmark_metadata": workload_resolution.get(
            "benchmark_metadata"
        ),
    }


# -----------------------------------
# Resolve Custom Workload
# -----------------------------------

@router.post(
    "/custom-comparison/resolve-workload"
)
def resolve_custom_workload(
    comparison: CustomAnalysisComparisonCreate,
    db: Session = Depends(get_db),
):

    reference_language = db.query(
        ProgrammingLanguage
    ).filter(
        ProgrammingLanguage.lang_id
        == comparison.reference_lang_id
    ).first()

    if reference_language is None:
        raise HTTPException(
            status_code=404,
            detail="Reference programming language not found.",
        )

    input_contract = detect_input_contract(
        reference_code=comparison.reference_code,
        language=reference_language.lang_name,
    )

    result = resolve_benchmark_workload(
        benchmark_name=(
            comparison.custom_benchmark_name
        ),
        description=(
            comparison.custom_description
        ),
        reference_code=(
            comparison.reference_code
        ),
        workload_type=(
            comparison.workload_type
        ),
        input_contract=input_contract,
    )

    return {
        "status": result.get(
            "status"
        ),
        "workload_type": result.get(
            "workload_type"
        ),
        "schema": result.get(
            "schema"
        ),
        "input_structure": result.get(
            "input_structure"
        ),
        "algorithm": result.get(
            "algorithm"
        ),
        "benchmark_metadata": result.get(
            "benchmark_metadata"
        ),
        "detection": result.get(
            "detection"
        ),
        "can_generate": result.get(
            "can_generate",
            False,
        ),
        "generation_mode": result.get(
            "generation_mode",
            "custom",
        ),
        "reason": (
            result.get("reason")
            or result.get(
                "detection",
                {},
            ).get("reason")
        ),
    }









# -----------------------------------
# Start Custom Benchmark Job
# -----------------------------------

@router.post(
    "/custom-comparison/start"
)
def start_custom_comparison(
    comparison: CustomAnalysisComparisonCreate,
    db: Session = Depends(get_db),
):

    if not comparison.target_lang_ids:
        raise HTTPException(
            status_code=400,
            detail=(
                "Select at least one "
                "target language."
            )
        )

    reference_language = (
        db.query(ProgrammingLanguage)
        .filter(
            ProgrammingLanguage.lang_id
            == comparison.reference_lang_id
        )
        .first()
    )

    if reference_language is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Reference programming language "
                "not found."
            ),
        )

    if not comparison.reference_code.strip():
        raise HTTPException(
            status_code=400,
            detail=(
                "Reference code cannot be empty."
            )
        )

    input_contract, resolved_workload = (
        validate_custom_input_mode(
            comparison=comparison,
            reference_language_name=(
                reference_language.lang_name
            ),
        )
    )

    job_id = str(
        uuid.uuid4()
    )

    now = (
        datetime.utcnow().isoformat()
    )

    with CUSTOM_ANALYSIS_JOBS_LOCK:

        CUSTOM_ANALYSIS_JOBS[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "current_step": None,
            "steps": {},
            "results": None,
            "error": None,
            "benchmark_metadata": (
                resolved_workload.get(
                    "benchmark_metadata"
                )
            ),
            "generation_mode": (
                resolved_workload.get(
                    "generation_mode",
                    "custom",
                )
            ),
            "can_generate": bool(
                resolved_workload.get(
                    "can_generate",
                    False,
                )
            ),
            "input_contract": input_contract,
            "workload_resolution": resolved_workload,
            "comparison_id": None,
            "created_at": now,
            "updated_at": now,
        }

    comparison_data = (
        comparison.model_dump()
    )

    # Propagate the resolver-selected workload type
    # into the worker so the benchmark engine uses
    # the resolved workload rather than only the raw
    # request value.
    resolved_workload_type = resolved_workload.get(
        "workload_type"
    )

    if resolved_workload_type:
        comparison_data["workload_type"] = (
            resolved_workload_type
        )

    comparison_data["input_contract"] = (
        input_contract
    )

    comparison_data["workload_resolution"] = (
        resolved_workload
    )

    comparison_data["benchmark_metadata"] = (
        resolved_workload.get(
            "benchmark_metadata"
        )
    )

    comparison_data["generation_mode"] = (
        resolved_workload.get(
            "generation_mode",
            "custom",
        )
    )

    comparison_data["can_generate"] = bool(
        resolved_workload.get(
            "can_generate",
            False,
        )
    )

    worker = threading.Thread(
        target=run_custom_analysis_job,
        args=(
            job_id,
            comparison_data,
        ),
        daemon=True,
    )

    worker.start()

    return {
        "job_id": job_id,
        "status": "queued",
        "workload_type": comparison_data.get(
            "workload_type"
        ),
        "generation_mode": comparison_data.get(
            "generation_mode",
            "custom",
        ),
        "can_generate": comparison_data.get(
            "can_generate",
            False,
        ),
        "benchmark_metadata": comparison_data.get(
            "benchmark_metadata"
        ),
        "input_contract": input_contract,
    }


# -----------------------------------
# Get Custom Benchmark Job Status
# -----------------------------------

@router.get(
    "/custom-comparison/status/{job_id}"
)
def get_custom_comparison_status(
    job_id: str,
):

    with CUSTOM_ANALYSIS_JOBS_LOCK:

        job = CUSTOM_ANALYSIS_JOBS.get(
            job_id
        )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Custom benchmark job "
                    "not found."
                )
            )

        return {
            "job_id":
                job["job_id"],

            "status":
                job["status"],
            "comparison_id": job.get(
                "comparison_id"
            ),
            "current_step":
                job["current_step"],

            "steps":
                dict(job["steps"]),

            "results":
                job["results"],

            
            "benchmark_metadata": job.get(
                "benchmark_metadata"
            ),

            "generation_mode": job.get(
                "generation_mode",
                "custom",
            ),

            "can_generate": job.get(
                "can_generate",
                False,
            ),

            "input_contract": job.get(
                "input_contract"
            ),

            "error":
                job["error"],

            "created_at":
                job["created_at"],

            "updated_at":
                job["updated_at"],
        }
    

# -----------------------------------
# Create Custom Benchmark Comparison
# -----------------------------------

@router.post(
    "/custom-comparison",
    response_model=list[AnalysisResponse]
)
def create_custom_comparison(
    comparison: CustomAnalysisComparisonCreate,
    db: Session = Depends(get_db),
):

    # -----------------------------------
    # Validate target languages
    # -----------------------------------

    if not comparison.target_lang_ids:
        raise HTTPException(
            status_code=400,
            detail="Select at least one target language."
        )

    # -----------------------------------
    # Find reference language
    # -----------------------------------

    reference_language = (
        db.query(ProgrammingLanguage)
        .filter(
            ProgrammingLanguage.lang_id
            == comparison.reference_lang_id
        )
        .first()
    )

    if reference_language is None:
        raise HTTPException(
            status_code=404,
            detail="Reference programming language not found."
        )

        # -----------------------------------
    # Exact input contract
    # -----------------------------------

    input_contract, resolved_workload = (
        validate_custom_input_mode(
            comparison=comparison,
            reference_language_name=(
                reference_language.lang_name
            ),
        )
    )
    # -----------------------------------
    # Find target languages
    # -----------------------------------

    target_languages = []

    target_ids = list(
        dict.fromkeys(
            comparison.target_lang_ids
        )
    )

    for lang_id in target_ids:

        if lang_id == comparison.reference_lang_id:
            continue

        language = (
            db.query(ProgrammingLanguage)
            .filter(
                ProgrammingLanguage.lang_id
                == lang_id
            )
            .first()
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Programming language {lang_id} "
                    "not found."
                )
            )

        target_languages.append(
            language.lang_name
        )

    if not target_languages:
        raise HTTPException(
            status_code=400,
            detail="Select at least one target language."
        )

    has_custom_input = bool(
    comparison.custom_input
    and comparison.custom_input.strip()
    )

    if not has_custom_input:
        if (
            comparison.input_size is None
            or comparison.input_size <= 0
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Input size must be greater than zero "
                    "when automatic workload generation is used."
                )
            )

    # -----------------------------------
    # Run custom benchmark
    # -----------------------------------

    try:

        benchmark_result = run_custom_benchmark(
            benchmark_name=(
                comparison.custom_benchmark_name
            ),
            benchmark_category=(
                comparison.custom_category
            ),
            description=(
                comparison.custom_description
            ),
            workload_type=(
                resolved_workload.get(
                    "workload_type"
                )
                or comparison.workload_type
            ),
            input_size=(
                comparison.input_size
            ),
            custom_input=(
                comparison.custom_input
            ),
            reference_language=(
                reference_language.lang_name
            ),
            reference_code=(
                comparison.reference_code
            ),
            target_languages=(
                target_languages
            ),
            input_contract=input_contract,
        )
        benchmark_metadata = benchmark_result.get(
            "benchmark_metadata"
        )

        resolved_benchmark_name = benchmark_result.get(
            "benchmark_name"
        )

        resolved_benchmark_category = benchmark_result.get(
            "benchmark_category"
        )

        resolved_description = benchmark_result.get(
            "description"
        )

        results = benchmark_result.get(
            "results",
            []
        )

    except (
        ValueError,
        FileNotFoundError,
        RuntimeError,
        TimeoutError,
    ) as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    # -----------------------------------
    # Convert custom results to Green Score format
    # -----------------------------------

    raw_results = []
    skipped_results = []

    for result in results:

        result_status = result.get(
            "status",
            "success",
        )

        if result_status != "success":
            skipped_results.append({
                "language": result.get("language"),
                "status": result_status,
                "reason": result.get(
                    "reason",
                    "Implementation did not complete successfully.",
                ),
            })
            continue

        language_name = result.get("language")

        if not language_name:
            skipped_results.append({
                "language": None,
                "status": "failed",
                "reason": "Benchmark result did not include a language.",
            })
            continue

        language = (
            db.query(ProgrammingLanguage)
            .filter(
                ProgrammingLanguage.lang_name
                == language_name
            )
            .first()
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Programming language "
                    f"{language_name} not found."
                )
            )

        execution_time = result.get(
            "execution_time"
        )
        cpu_usage = result.get(
            "cpu_usage"
        )
        memory_usage = result.get(
            "memory_usage"
        )
        energy_consumption = result.get(
            "energy_consumption"
        )
        output_verified = result.get(
            "output_verified",
            False,
        )

        missing_metrics = []

        if execution_time is None:
            missing_metrics.append(
                "execution_time"
            )

        if cpu_usage is None:
            missing_metrics.append(
                "cpu_usage"
            )

        if memory_usage is None:
            missing_metrics.append(
                "memory_usage"
            )

        if energy_consumption is None:
            missing_metrics.append(
                "energy_consumption"
            )

        if missing_metrics:
            skipped_results.append({
                "language": language_name,
                "status": "failed",
                "reason": (
                    "Missing benchmark metrics: "
                    + ", ".join(missing_metrics)
                ),
            })
            continue

        raw_results.append({
            "lang_id":
                language.lang_id,

            "execution_time":
                execution_time,

            "cpu_usage":
                cpu_usage,

            "memory_usage":
                memory_usage,

            "energy_consumption":
                energy_consumption,

            "output_verified":
                output_verified,
        })

    if not raw_results:
        raise HTTPException(
            status_code=400,
            detail=(
                "No implementation completed successfully, "
                "so no benchmark measurements are available."
            ),
        )

    # -----------------------------------
    # Calculate Green Scores
    # -----------------------------------

    scored_results = calculate_green_scores(
        raw_results
    )

    comparison_record = Comparison(
        user_id=comparison.user_id,
        comparison_type="custom",
        bench_id=None,
        bench_size=None,
        custom_category=(
            resolved_benchmark_category
        ),
        custom_benchmark_name=(
            resolved_benchmark_name
        ),
        workload_type=(
            resolved_workload.get(
                "workload_type"
            )
            or comparison.workload_type
        ),
        input_size=(
            comparison.input_size
        ),
    )

    db.add(comparison_record)
    db.commit()
    db.refresh(comparison_record)

    # -----------------------------------
    # Save custom analysis results
    # -----------------------------------

    saved_results = []

    for result in scored_results:

        analysis_data = AnalysisCreate(
            user_id=comparison.user_id,

            analysis_type="custom",

            bench_id=None,
            comparison_id=(
                comparison_record.comparison_id
            ),
            lang_id=result["lang_id"],

            bench_size=None,

            custom_category=(
                resolved_benchmark_category
            ),

           custom_benchmark_name=(
                resolved_benchmark_name
            ),

            custom_description=(
                resolved_description
            ),
            benchmark_metadata=benchmark_metadata,
            workload_type=(
                resolved_workload.get(
                    "workload_type"
                )
                or comparison.workload_type
            ),
            input_size=(
                comparison.input_size
            ),
        )

        saved_analysis = (
            analysis_service.create_analysis(
                db=db,

                analysis=analysis_data,

                execution_time=(
                    result["execution_time"]
                ),

                cpu_usage=(
                    result["cpu_usage"]
                ),

                memory_usage=(
                    result["memory_usage"]
                ),

                energy_consumption=(
                    result["energy_consumption"]
                ),

                green_score=(
                    result.get(
                        "green_score"
                    )
                ),

                green_score_label=(
                    result.get(
                        "green_score_label"
                    )
                ),

                output_verified=(
                    result["output_verified"]
                ),
            )
        )

        saved_results.append(
            saved_analysis
        )

    return saved_results

# -----------------------------------
# Get All Analysis
# -----------------------------------
@router.get(
    "/",
    response_model=list[AnalysisResponse]
)
def get_all_analysis(
    db: Session = Depends(get_db)
):
    return analysis_service.get_all_analyses(db)


# -----------------------------------
# Get Analysis By ID
# -----------------------------------
@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse
)
def get_analysis_by_id(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    analysis = analysis_service.get_analysis_by_id(
        db,
        analysis_id
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return analysis


# -----------------------------------
# Get Analysis By User
# -----------------------------------
@router.get(
    "/user/{user_id}",
    response_model=list[AnalysisResponse]
)
def get_analysis_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return analysis_service.get_analysis_by_user(
        db,
        user_id
    )


# -----------------------------------
# Delete Analysis
# -----------------------------------
@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):

    analysis = analysis_service.delete_analysis(
        db,
        analysis_id
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return {
        "message": "Analysis deleted successfully."
    }