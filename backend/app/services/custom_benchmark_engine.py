from pathlib import Path
import os
import tempfile
import shutil


# ============================================================
# OPTIONAL AI CODE GENERATION
# ============================================================
# Disabled by default. Automatic Benchmark Metadata Intelligence
# must remain deterministic and must never require an external LLM.
# Set ENABLE_AI_CODE_GENERATION=true only when the optional
# cross-language generation feature is intentionally enabled.
ENABLE_AI_CODE_GENERATION = (
    os.getenv("ENABLE_AI_CODE_GENERATION", "false")
    .strip()
    .lower()
    in {"1", "true", "yes", "on"}
)

from app.services.compiler_runner import (
    compile_program,
)
from app.services.custom_workload_generator import (
    generate_workload,
    generate_from_input_contract,
)
from app.services.workload_resolver import (
    resolve_benchmark_workload,
)

from app.services.metrics_monitor import (
    execute_with_monitor,
)

# from app.services.ai_code_generation_service import (
#     generate_equivalent_code,
# )


# ============================================================
# LANGUAGE CONFIG
# ============================================================

LANGUAGE_NAME_MAP = {
    "c": "c",
    "c++": "cpp",
    "java": "java",
    "python": "python",
    "javascript": "javascript",
    "go": "go",
    "rust": "rust",
    "c#": "csharp",
    "kotlin": "kotlin",
    "php": "php",
}


LANGUAGE_EXTENSIONS = {
    "c": ".c",
    "cpp": ".cpp",
    "java": ".java",
    "python": ".py",
    "javascript": ".js",
    "go": ".go",
    "rust": ".rs",
    "csharp": ".cs",
    "kotlin": ".kt",
    "php": ".php",
}


# ============================================================
# NORMALIZE LANGUAGE
# ============================================================

def normalize_language(
    language_name: str
) -> str:

    key = language_name.lower().strip()

    language = LANGUAGE_NAME_MAP.get(
        key
    )

    if language is None:
        raise ValueError(
            f"Unsupported language: {language_name}"
        )

    return language


# ============================================================
# GENERATE COMMON INPUT
# ============================================================

def generate_custom_input(
    input_size: int,
    seed: int = 42,
) -> str:

    return generate_workload(
        workload_type="numeric-array",
        input_size=input_size,
        seed=seed,
    )

# ============================================================
# GENERATE INPUT FROM CUSTOM WORKLOAD SCHEMA
# ============================================================

def generate_schema_input(
    workload_type: str,
    schema: dict,
    input_size: int | None,
    seed: int = 42,
) -> str:
    """
    Deterministically generate input for workloads that are
    recognized by the resolver but are not yet represented
    by the main WORKLOAD_REGISTRY.

    This function does NOT execute code.
    It only creates stdin input.
    """

    import random

    rng = random.Random(seed)

    if not schema:
        raise ValueError(
            "Custom workload schema is missing."
        )

    normalized_type = (
        workload_type
        or "custom"
    ).strip().lower()

    size = (
        input_size
        if input_size is not None
        else 10
    )

    size = max(1, int(size))

    # --------------------------------------------------------
    # CHARACTERS
    # --------------------------------------------------------

    if normalized_type in {
        "characters",
        "character-array",
    }:

        characters = [
            "a", "b", "c", "d", "e",
            "f", "g", "h", "i", "j",
        ]

        values = [
            rng.choice(characters)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # FLOAT / DECIMAL
    # --------------------------------------------------------

    if normalized_type in {
        "float-array",
        "floating-point",
        "decimal",
        "decimal-array",
    }:

        values = [
            f"{rng.uniform(0.1, 100.0):.3f}"
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
# BOOLEAN
# Canonical stdin format:
# n
# 1 0 1 1 0 ...
# --------------------------------------------------------

    if normalized_type in {
        "boolean",
        "boolean-array",
        "bool-array",
    }:

        values = [
            str(rng.choice([0, 1]))
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # ARRAY + TARGET
    # --------------------------------------------------------

    if normalized_type in {
        "array-plus-target",
        "array-target",
    }:

        values = [
            rng.randint(1, 100)
            for _ in range(size)
        ]

        target = (
            values[0] + values[1]
            if len(values) >= 2
            else values[0]
        )

        return (
            f"{size}\n"
            + " ".join(map(str, values))
            + "\n"
            + f"{target}\n"
        )

    # --------------------------------------------------------
    # MULTIPLE TEST CASES
    # --------------------------------------------------------

    if normalized_type in {
        "multiple-test-cases",
        "test-cases",
    }:

        test_cases = min(
            max(size, 1),
            20,
        )

        lines = [str(test_cases)]

        for _ in range(test_cases):

            case_size = min(
                max(size, 1),
                100,
            )

            values = [
                rng.randint(1, 100)
                for _ in range(case_size)
            ]

            lines.append(
                str(case_size)
            )

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # PAIRS / TUPLES
    # --------------------------------------------------------

    if normalized_type in {
        "pairs",
        "tuples",
        "pairs-tuples",
    }:

        lines = [str(size)]

        for _ in range(size):

            x = rng.randint(1, 100)
            y = rng.randint(1, 100)

            lines.append(
                f"{x} {y}"
            )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # KEY-VALUE
    # --------------------------------------------------------

    if normalized_type in {
        "key-value",
        "key-value-data",
        "key-value-records",
    }:

        lines = [str(size)]

        for index in range(size):

            value = rng.randint(1, 100)

            lines.append(
                f"key{index + 1}={value}"
            )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # MIXED RECORDS
    # --------------------------------------------------------

    if normalized_type in {
        "mixed-records",
        "mixed-datatype-records",
    }:

        lines = [str(size)]

        for index in range(size):

            integer_value = rng.randint(
                1,
                100,
            )

            decimal_value = round(
                rng.uniform(
                    1.0,
                    100.0,
                ),
                2,
            )

            boolean_value = (
                "true"
                if rng.choice(
                    [True, False]
                )
                else "false"
            )

            lines.append(
                f"{integer_value} "
                f"name{index + 1} "
                f"{decimal_value} "
                f"{boolean_value}"
            )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # DATE / TIME
    # --------------------------------------------------------

    if normalized_type in {
        "date",
        "datetime",
        "date-time",
        "timestamp",
    }:

        lines = [str(size)]

        for index in range(size):

            day = (
                index % 28
            ) + 1

            lines.append(
                f"2026-01-{day:02d} "
                f"12:00:00"
            )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # GENERIC ARRAY SCHEMA
    # --------------------------------------------------------

    schema_type = (
        schema.get("type")
    )

    item_type = (
        schema.get("item_type")
    )

    if schema_type == "array":

        count_field = (
            schema.get(
                "count_field"
            )
        )

        if item_type == "integer":

            values = [
                rng.randint(
                    1,
                    100,
                )
                for _ in range(size)
            ]

            return (
                f"{size}\n"
                + " ".join(
                    map(str, values)
                )
                + "\n"
            )

        if item_type == "float":

            values = [
                f"{rng.uniform(1, 100):.3f}"
                for _ in range(size)
            ]

            return (
                f"{size}\n"
                + " ".join(values)
                + "\n"
            )

        if item_type == "character":

            values = [
                rng.choice(
                    "abcdefghijklmnopqrstuvwxyz"
                )
                for _ in range(size)
            ]

            return (
                f"{size}\n"
                + " ".join(values)
                + "\n"
            )

    # --------------------------------------------------------
    # GENERIC COMPOSITE SCHEMA
    # --------------------------------------------------------

    if schema_type == "composite":

        fields = schema.get(
            "fields",
            [],
        )

        lines = []

        for field in fields:

            field_type = field.get(
                "type"
            )

            if field_type == "integer":

                lines.append(
                    str(size)
                )

            elif field_type == "integer[]":

                values = [
                    rng.randint(
                        1,
                        100,
                    )
                    for _ in range(size)
                ]

                lines.append(
                    " ".join(
                        map(
                            str,
                            values,
                        )
                    )
                )

            elif field_type == "float":

                lines.append(
                    "10.5"
                )

            elif field_type == "string":

                lines.append(
                    "sample"
                )

            elif field_type == "boolean":

                lines.append(
                    "true"
                )

            else:

                lines.append(
                    "sample"
                )

        return "\n".join(lines) + "\n"

    # --------------------------------------------------------
    # SAFE FALLBACK
    # --------------------------------------------------------

    raise ValueError(
        "A workload schema was detected, but no deterministic "
        f"generator is currently available for workload type "
        f"'{normalized_type}'. Please provide Custom Input."
    )

# ============================================================
# CREATE SOURCE FILE
# ============================================================

def create_source_file(
    directory: str,
    language: str,
    code: str,
) -> Path:

    extension = (
        LANGUAGE_EXTENSIONS[
            language
        ]
    )

    source_file = (
        Path(directory)
        / f"source{extension}"
    )

    source_file.write_text(
        code,
        encoding="utf-8"
    )

    return source_file


# ============================================================
# RUN ONE IMPLEMENTATION
# ============================================================

def run_custom_code(
    language_name: str,
    source_code: str,
    input_data: str,
):
    """
    Compile and run one custom implementation.

    Never raises compilation/runtime/timeout failures to the
    benchmark orchestration layer. Returns a structured result
    so reference and target failures can be handled independently.
    """

    language = normalize_language(language_name)

    temp_dir = tempfile.mkdtemp(
        prefix="greencode_custom_"
    )

    try:
        source_file = create_source_file(
            directory=temp_dir,
            language=language,
            code=source_code,
        )

        try:
            command = compile_program(
                language=language,
                source_file=str(source_file),
                output_dir=temp_dir,
            )
        except Exception as exc:
            return {
                "status": "compile_error",
                "error": str(exc),
                "execution_time": None,
                "cpu_usage": None,
                "memory_usage": None,
                "energy_consumption": None,
                "stdout": "",
                "stderr": str(exc),
                "return_code": None,
            }

        try:
            result = execute_with_monitor(
                command=command,
                input_data=input_data,
                timeout=120,
            )
        except TimeoutError as exc:
            return {
                "status": "timeout",
                "error": str(exc) or "Execution timed out.",
                "execution_time": None,
                "cpu_usage": None,
                "memory_usage": None,
                "energy_consumption": None,
                "stdout": "",
                "stderr": str(exc),
                "return_code": None,
            }
        except Exception as exc:
            return {
                "status": "runtime_error",
                "error": str(exc),
                "execution_time": None,
                "cpu_usage": None,
                "memory_usage": None,
                "energy_consumption": None,
                "stdout": "",
                "stderr": str(exc),
                "return_code": None,
            }

        return {
            "status": (
                "success"
                if result.get("return_code") == 0
                else "runtime_error"
            ),
            "error": (
                None
                if result.get("return_code") == 0
                else (
                    result.get("stderr")
                    or "Program exited with a non-zero return code."
                )
            ),
            "execution_time": result.get("execution_time"),
            "cpu_usage": result.get("cpu_usage"),
            "memory_usage": result.get("memory_usage"),
            "energy_consumption": result.get(
                "energy_consumption"
            ),
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "return_code": result.get("return_code"),
        }

    except Exception as exc:
        return {
            "status": "execution_error",
            "error": str(exc),
            "execution_time": None,
            "cpu_usage": None,
            "memory_usage": None,
            "energy_consumption": None,
            "stdout": "",
            "stderr": str(exc),
            "return_code": None,
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )


# ============================================================
# VERIFY OUTPUT
# ============================================================

def verify_output(
    reference_output: str,
    target_output: str,
) -> bool:
    """
    Compare normalized stdout values.

    Execution success/failure is handled by the caller.
    This function only compares actual outputs.
    """

    if reference_output is None:
        reference_output = ""

    if target_output is None:
        target_output = ""

    return (
        reference_output.strip()
        ==
        target_output.strip()
    )


# ============================================================
# RUN CUSTOM BENCHMARK
# ============================================================

def run_custom_benchmark(
    benchmark_name: str,
    benchmark_category: str,
    description: str | None,

    workload_type: str | None = None,
    input_size: int | None = None,

    reference_language: str = "",
    reference_code: str = "",

    target_languages: list[str] | None = None,

    progress_callback=None,
    custom_input=None,
    input_contract: dict | None = None,
):

    """
    Complete custom benchmark workflow.
    """

    def report_progress(
        step: str,
        status: str,
        message: str,
    ):

        if progress_callback is not None:
            try:
                progress_callback({
                    "step": step,
                    "status": status,
                    "message": message,
                })
            except Exception:
                # Progress reporting must never interrupt
                # the benchmark execution pipeline.
                pass

    # --------------------------------------------------------
    # Validate request
    # --------------------------------------------------------

    if not reference_code.strip():
        raise ValueError(
            "Reference code cannot be empty."
        )

    if not target_languages:
        raise ValueError(
            "Select at least one target language."
        )

    report_progress(
        step="validate",
        status="completed",
        message="Benchmark request validated",
    )

    # --------------------------------------------------------
    # Generate common input
    # --------------------------------------------------------

    report_progress(
        step="input",
        status="processing",
        message="Preparing input workload",
    )
    resolved_workload = resolve_benchmark_workload(
        benchmark_name=benchmark_name,
        description=description,
        reference_code=reference_code,
        workload_type=workload_type,
        input_contract=input_contract,
    )

    benchmark_metadata = resolved_workload.get("benchmark_metadata")

    if not isinstance(benchmark_metadata, dict):
        benchmark_metadata = {}

    resolved_benchmark_name = (
        benchmark_metadata.get("name")
        or benchmark_name
    )

    resolved_benchmark_category = (
        benchmark_metadata.get("category")
        or benchmark_category
    )

    resolved_description = (
        benchmark_metadata.get("description")
        or description
    )

    resolved_workload_type = (
        resolved_workload.get("workload_type")
    )

    input_data = resolve_benchmark_input(
        benchmark_name=benchmark_name,
        description=description,
        reference_code=reference_code,
        workload_type=resolved_workload_type,
        input_size=input_size,
        custom_input=custom_input,
        resolved_workload=resolved_workload,
        input_contract=input_contract,
    )

    report_progress(
        step="input",
        status="completed",
        message="Input workload prepared",
    )

    # --------------------------------------------------------
    # Run reference implementation
    # --------------------------------------------------------

    report_progress(
        step="reference",
        status="processing",
        message=(
            f"Executing reference "
            f"{reference_language} implementation"
        ),
    )

    reference_result = run_custom_code(
        language_name=reference_language,
        source_code=reference_code,
        input_data=input_data,
    )

    if reference_result.get("status") != "success":
        report_progress(
            step="reference",
            status="failed",
            message=(
                f"Reference {reference_language} "
                f"implementation failed: "
                f"{reference_result.get('error') or 'Unknown error'}"
            ),
        )

        return {
            "benchmark_name": resolved_benchmark_name,
            "benchmark_category": resolved_benchmark_category,
            "description": resolved_description,
            "benchmark_metadata": benchmark_metadata,
            "results": [{
                "language": reference_language,
                "is_reference": True,
                "generated": False,
                "source_code": reference_code,
                "execution_time": reference_result.get(
                    "execution_time"
                ),
                "cpu_usage": reference_result.get(
                    "cpu_usage"
                ),
                "memory_usage": reference_result.get(
                    "memory_usage"
                ),
                "energy_consumption": reference_result.get(
                    "energy_consumption"
                ),
                "output": reference_result.get(
                    "stdout", ""
                ),
                "output_verified": False,
                "status": reference_result.get(
                    "status",
                    "execution_error"
                ),
                "error": reference_result.get(
                    "error"
                ),
            }],
            "status": "reference_failed",
            "error": (
                reference_result.get("error")
                or "Reference implementation failed."
            ),
        }

    report_progress(
        step="reference",
        status="completed",
        message=(
            f"Reference {reference_language} "
            f"implementation executed successfully"
        ),
    )

    reference_output = reference_result.get(
        "stdout",
        ""
    )

    results = []

    # --------------------------------------------------------
    # Add reference result
    # --------------------------------------------------------

    results.append({
        "language":
            reference_language,

        "is_reference":
            True,

        "generated":
            False,

        "source_code":
            reference_code,

        "execution_time":
            reference_result[
                "execution_time"
            ],

        "cpu_usage":
            reference_result[
                "cpu_usage"
            ],

        "memory_usage":
            reference_result[
                "memory_usage"
            ],

        "energy_consumption":
            reference_result[
                "energy_consumption"
            ],

        "output":
            reference_output,

        "output_verified":
            True,

        "status":
            reference_result.get(
                "status",
                "success"
            ),

        "error":
            reference_result.get(
                "error"
            ),
        })

    # --------------------------------------------------------
    # Generate and execute targets
    # --------------------------------------------------------

    for target_language in target_languages:

        if (
            target_language.lower().strip()
            ==
            reference_language.lower().strip()
        ):
            continue

        safe_language_name = (
            target_language
            .lower()
            .replace("+", "plus")
            .replace("#", "sharp")
            .replace(" ", "-")
        )

        generation_step = (
            f"generate-{safe_language_name}"
        )

        execution_step = (
            f"execute-{safe_language_name}"
        )

        # --------------------------------------------------------
        # OPTIONAL AI TARGET GENERATION
        # --------------------------------------------------------
        # Cross-language target generation is deliberately isolated
        # from the deterministic benchmark pipeline. When disabled,
        # no Gemini/LLM service is imported or invoked. The reference
        # benchmark still completes and the target receives an honest
        # explicit not-generated result.
        if not ENABLE_AI_CODE_GENERATION:
            results.append({
                "language": target_language,
                "is_reference": False,
                "generated": False,
                "source_code": None,
                "execution_time": None,
                "cpu_usage": None,
                "memory_usage": None,
                "energy_consumption": None,
                "output": None,
                "output_verified": False,
                "status": "not-generated",
                "reason": (
                    "Automatic target-language generation is "
                    "disabled. No AI code generation service "
                    "was invoked."
                ),
            })

            report_progress(
                step=generation_step,
                status="skipped",
                message=(
                    f"{target_language} implementation generation "
                    "skipped because AI code generation is disabled"
                ),
            )
            continue

        # AI is an explicit opt-in feature. Import lazily so a normal
        # benchmark run cannot initialize the Gemini client by accident.
        from app.services.ai_code_generation_service import (
            generate_equivalent_code,
        )

        # -----------------------------
        # Generate code
        # -----------------------------

        report_progress(
            step=generation_step,
            status="processing",
            message=(
                f"Generating "
                f"{target_language} implementation"
            ),
        )

        generated_code = generate_equivalent_code(
            reference_language=
                reference_language,

            target_language=
                target_language,

            reference_code=
                reference_code,

            benchmark_name=
                resolved_benchmark_name,

            benchmark_category=
                resolved_benchmark_category,

            description=
                resolved_description,

            workload_type=resolved_workload.get(
                "workload_type"
            ),

            input_size=
                input_size,
        )

        report_progress(
            step=generation_step,
            status="completed",
            message=(
                f"{target_language} "
                f"implementation generated"
            ),
        )

        # -----------------------------
        # Execute target
        # -----------------------------

        report_progress(
            step=execution_step,
            status="processing",
            message=(
                f"Executing and validating "
                f"{target_language} implementation"
            ),
        )

        



        target_result = run_custom_code(
            language_name=target_language,
            source_code=generated_code,
            input_data=input_data,
        )

        target_status = target_result.get(
            "status",
            "execution_error"
        )

        if target_status != "success":
            output_verified = False

            report_progress(
                step=execution_step,
                status="failed",
                message=(
                    f"{target_language} implementation "
                    f"failed: "
                    f"{target_result.get('error') or 'Unknown error'}"
                ),
            )

        else:
            output_verified = verify_output(
                reference_output=reference_output,
                target_output=target_result.get(
                    "stdout",
                    ""
                ),
            )

            if output_verified:
                report_progress(
                    step=execution_step,
                    status="completed",
                    message=(
                        f"{target_language} implementation "
                        f"executed and verified"
                    ),
                )
            else:
                report_progress(
                    step=execution_step,
                    status="failed",
                    message=(
                        f"{target_language} output "
                        f"does not match reference"
                    ),
                )

        if output_verified:

            report_progress(
                step=execution_step,
                status="completed",
                message=(
                    f"{target_language} implementation "
                    f"executed and verified"
                ),
            )

        else:

            report_progress(
                step=execution_step,
                status="failed",
                message=(
                    f"{target_language} output "
                    f"does not match reference"
                ),
            )

        results.append({
            "language":
                target_language,

            "is_reference":
                False,

            "generated":
                True,

            "source_code":
                generated_code,

            "execution_time":
                target_result[
                    "execution_time"
                ],

            "cpu_usage":
                target_result[
                    "cpu_usage"
                ],

            "memory_usage":
                target_result[
                    "memory_usage"
                ],

            "energy_consumption":
                target_result[
                    "energy_consumption"
                ],

            "output":
                target_result.get(
                    "stdout",
                    ""
                ),

            "output_verified":
                output_verified,

            "status":
                target_status,

            "error":
                target_result.get(
                    "error"
                ),
        })

    return {
        "benchmark_name": resolved_benchmark_name,
        "benchmark_category": resolved_benchmark_category,
        "description": resolved_description,
        "benchmark_metadata": benchmark_metadata,
        "results": results,
    }



def resolve_benchmark_input(
    benchmark_name: str,
    description: str | None,
    reference_code: str,
    workload_type: str | None,
    input_size: int | None,
    custom_input: str | None = None,
    resolved_workload: dict | None = None,
    input_contract: dict | None = None,
):
    """
    Resolve the exact workload input that will be supplied
    to every language implementation.

    Priority:

        1. User-provided custom input
        2. Known workload registry generator
        3. Deterministic custom-schema generator
        4. Safe failure when no structure can be generated
    """

    # --------------------------------------------------------
    # USER PROVIDED INPUT
    # --------------------------------------------------------

    if (
        custom_input is not None
        and custom_input.strip()
    ):

        return custom_input


    # --------------------------------------------------------
    # RESOLVE WORKLOAD STRUCTURE
    # --------------------------------------------------------

    workload = resolved_workload

    if workload is None:
        workload = resolve_benchmark_workload(
            benchmark_name=benchmark_name,
            description=description,
            reference_code=reference_code,
            workload_type=workload_type,
            input_contract=input_contract,
        )


    # --------------------------------------------------------
    # RESOLVED INPUT CONTRACT / WORKLOAD
    # --------------------------------------------------------

    resolved_type = workload.get(
        "workload_type"
    )

    schema = workload.get(
        "schema"
    )

    capability = workload.get(
        "can_generate",
        False,
    )

    # Exact Input Contract is authoritative.
    # A "known" structure does not necessarily mean that
    # WORKLOAD_REGISTRY already has a generator for it.

    if (
        input_contract is not None
        and input_contract.get("contract_type")
    ):

        contract_type = (
            input_contract.get(
                "contract_type"
            )
        )

        # No stdin required.
        if contract_type == "no-input":
            return ""

        # --------------------------------------------------------
        # EXACT CONTRACT GENERATOR — AUTHORITATIVE PATH
        # --------------------------------------------------------
        # The Input Contract Analyzer describes the actual function/input
        # interface. That contract must be handed directly to the
        # deterministic contract generator. Do NOT force it through the
        # legacy schema generator: a valid contract can exist even when
        # the resolver has no registry/schema entry.
        if input_size is None:
            raise ValueError(
                "Input size is required when "
                "generating workload automatically."
            )

        algorithm = workload.get("algorithm")
        algorithm_name = (
            algorithm.get("name")
            if isinstance(algorithm, dict)
            else None
        )

        return generate_from_input_contract(
            input_contract=input_contract,
            input_size=input_size,
            seed=42,
            algorithm=algorithm_name,
        )

        # Exact contract is known, but no deterministic generator exists.
        raise ValueError(
            "The exact input contract was detected, "
            f"but no deterministic generator is available "
            f"for contract '{contract_type}'."
        )


    # --------------------------------------------------------
    # LEGACY / NON-CONTRACT WORKLOAD
    # --------------------------------------------------------

    if (
    workload.get("status") == "known"
    and resolved_type
    and capability
    ):

        if input_size is None:
            raise ValueError(
                "Input size is required when "
                "generating workload automatically."
            )

        return generate_workload(
            workload_type=resolved_type,
            input_size=input_size,
            seed=42,
        )


    if schema:
        return generate_schema_input(
            workload_type=resolved_type,
            schema=schema,
            input_size=input_size,
            seed=42,
        )

    # --------------------------------------------------------
    # UNKNOWN WORKLOAD
    # --------------------------------------------------------

    raise ValueError(
        "The workload structure could not be resolved "
        "automatically. Please provide Custom Input."
    )



def resolve_workload_type(
    benchmark_name: str,
    description: str | None,
    reference_code: str,
    workload_type: str | None,
    input_contract: dict | None = None,
) -> str:
    
    workload = resolve_benchmark_workload(
        benchmark_name=benchmark_name,
        description=description,
        reference_code=reference_code,
        workload_type=workload_type,
        input_contract=input_contract,
    )

    resolved_type = workload.get(
    "workload_type"
    )

    if not resolved_type:
        raise ValueError(
            "The workload type could not be resolved."
        )

    return resolved_type
