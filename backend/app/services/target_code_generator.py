from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_BASE_URL = (
    os.getenv(
        "OLLAMA_BASE_URL",
        "http://127.0.0.1:11434",
    )
    .strip()
    .rstrip("/")
)

OLLAMA_MODEL = (
    os.getenv(
        "OLLAMA_CODE_MODEL",
        "qwen2.5-coder:7b",
    )
    .strip()
)

OLLAMA_TIMEOUT_SECONDS = int(
    os.getenv(
        "OLLAMA_CODE_TIMEOUT_SECONDS",
        "180",
    )
)

OLLAMA_NUM_PREDICT = int(
    os.getenv(
        "OLLAMA_CODE_NUM_PREDICT",
        "1024",
    )
)

OLLAMA_NUM_CTX = int(
    os.getenv(
        "OLLAMA_CODE_NUM_CTX",
        "4096",
    )
)


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

SUPPORTED_LANGUAGES = {
    "C",
    "C++",
    "Java",
    "Python",
    "JavaScript",
    "Go",
    "Rust",
    "C#",
    "Kotlin",
    "PHP",
}


# ============================================================
# LANGUAGE NAME NORMALIZATION
# ============================================================

_LANGUAGE_ALIASES = {
    "c": "C",
    "cpp": "C++",
    "c++": "C++",
    "java": "Java",
    "python": "Python",
    "py": "Python",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "node": "JavaScript",
    "nodejs": "JavaScript",
    "go": "Go",
    "golang": "Go",
    "rust": "Rust",
    "c#": "C#",
    "csharp": "C#",
    "cs": "C#",
    "kotlin": "Kotlin",
    "php": "PHP",
}


def _normalize_language_name(
    language: str,
) -> str:
    normalized = (
        str(language or "")
        .strip()
        .lower()
    )

    return _LANGUAGE_ALIASES.get(
        normalized,
        str(language or "").strip(),
    )


# ============================================================
# FORMAT STRUCTURED DATA FOR PROMPT
# ============================================================

def _format_json_for_prompt(
    value: Any,
) -> str:
    if value is None:
        return "Not available."

    try:
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return str(value)


# ============================================================
# ALGORITHM METADATA EXTRACTION
# ============================================================

def _extract_algorithm_metadata(
    benchmark_metadata: dict[str, Any] | None,
    resolved_workload: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Read algorithm information already produced by GreenCode.

    This function does NOT perform algorithm detection.
    The reference source remains the primary semantic authority.
    """

    if isinstance(resolved_workload, dict):
        algorithm = resolved_workload.get(
            "algorithm"
        )

        if isinstance(algorithm, dict):
            return algorithm

    if isinstance(benchmark_metadata, dict):
        algorithm = benchmark_metadata.get(
            "algorithm"
        )

        if isinstance(algorithm, dict):
            return algorithm

    return {}


# ============================================================
# COMPLEXITY METADATA EXTRACTION
# ============================================================

def _extract_complexity_metadata(
    benchmark_metadata: dict[str, Any] | None,
    resolved_workload: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Read complexity information already produced by
    GreenCode's algorithm/workload intelligence.

    Complexity may be nested inside the resolved algorithm
    metadata, which is the preferred source.
    """

    # --------------------------------------------------------
    # PREFERRED:
    # resolved_workload["algorithm"]["complexity"]
    # --------------------------------------------------------

    if isinstance(resolved_workload, dict):

        algorithm = resolved_workload.get(
            "algorithm"
        )

        if isinstance(algorithm, dict):

            complexity = algorithm.get(
                "complexity"
            )

            if isinstance(complexity, dict):
                return complexity

        # Backward-compatible fallback.
        complexity = resolved_workload.get(
            "complexity"
        )

        if isinstance(complexity, dict):
            return complexity

    # --------------------------------------------------------
    # METADATA FALLBACK
    # --------------------------------------------------------

    if isinstance(benchmark_metadata, dict):

        algorithm = benchmark_metadata.get(
            "algorithm"
        )

        if isinstance(algorithm, dict):

            complexity = algorithm.get(
                "complexity"
            )

            if isinstance(complexity, dict):
                return complexity

        complexity = benchmark_metadata.get(
            "complexity"
        )

        if isinstance(complexity, dict):
            return complexity

    return {}

# ============================================================
# ALGORITHM-SPECIFIC PRESERVATION RULES
# ============================================================

def _get_algorithm_preservation_requirements(
    algorithm: dict[str, Any],
) -> str:
    """
    Add restrictions only when GreenCode has identified a
    sufficiently specific algorithm.

    These rules guide generation. Final correctness is still
    established by compile/run/output verification downstream.
    """

    algorithm_name = str(
        algorithm.get("name")
        or algorithm.get("algorithm_name")
        or ""
    ).strip().lower()

    common_rules = [
        (
            "Preserve the algorithmic strategy and control-flow "
            "behavior of the reference implementation."
        ),
        (
            "Preserve the important data structures used by the "
            "reference algorithm unless the target language requires "
            "a direct idiomatic equivalent."
        ),
        (
            "Do not replace the reference algorithm with a built-in "
            "library algorithm that performs the core benchmark work."
        ),
        (
            "Do not introduce a fundamentally different algorithm "
            "even if it produces the same output."
        ),
        (
            "Preserve early termination, first-match behavior, "
            "ordering behavior, and mutation behavior when they are "
            "semantically relevant in the reference implementation."
        ),
    ]

    specific_rules: dict[str, list[str]] = {
        "linear-search": [
            (
                "Perform a sequential linear scan of the search "
                "space."
            ),
            (
                "Do not sort the input before searching."
            ),
            (
                "Do not use binary search."
            ),
            (
                "Do not use hashing, maps, sets, or lookup tables "
                "to replace the sequential search."
            ),
            (
                "Do not use built-in search/index operations such "
                "as std::find, ranges::find, indexOf, findIndex, "
                "Array.IndexOf, list.index, or equivalent APIs to "
                "perform the benchmarked search."
            ),
        ],

        "binary-search": [
            (
                "Implement binary search explicitly using the same "
                "iterative or recursive strategy as the reference "
                "when that strategy is evident."
            ),
            (
                "Do not replace binary search with linear search, "
                "hash lookup, or a built-in binary-search API."
            ),
            (
                "Do not change the reference program's duplicate "
                "element handling or match-selection behavior."
            ),
        ],

        "bubble-sort": [
            (
                "Implement Bubble Sort explicitly using repeated "
                "adjacent comparisons and swaps."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
            (
                "Preserve any early-exit optimization present in "
                "the reference implementation."
            ),
        ],

        "insertion-sort": [
            (
                "Implement Insertion Sort explicitly by inserting "
                "elements into the already processed prefix."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
        ],

        "selection-sort": [
            (
                "Implement Selection Sort explicitly by selecting "
                "the required minimum/maximum element for each "
                "position."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
        ],

        "merge-sort": [
            (
                "Implement Merge Sort explicitly using divide, "
                "recursive/structural sorting, and merge operations."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
        ],

        "quick-sort": [
            (
                "Implement Quick Sort explicitly using partitioning "
                "and recursive/structural subproblem processing."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
            (
                "Preserve the reference partition/pivot strategy "
                "when it is evident from the source."
            ),
        ],

        "heap-sort": [
            (
                "Implement Heap Sort explicitly using heap "
                "construction and heap restoration operations."
            ),
            (
                "Do not use a built-in sorting function or another "
                "sorting algorithm."
            ),
        ],
    }

    rules = list(common_rules)

    rules.extend(
        specific_rules.get(
            algorithm_name,
            [],
        )
    )

    return "\n".join(
        f"- {rule}"
        for rule in rules
    )


# ============================================================
# TARGET LANGUAGE REQUIREMENTS
# ============================================================

def _get_language_requirements(
    target_language: str,
) -> str:
    requirements = {
        "C": [
            "Produce a complete C program.",
            "Use standard input for all benchmark input.",
            "Use standard output only for the expected result.",
            "Use portable standard C constructs where practical.",
        ],

        "C++": [
            "Produce a complete C++17-compatible program.",
            "Use standard input for all benchmark input.",
            "Use standard output only for the expected result.",
            (
                "Parse numeric input as numeric values, never as "
                "raw character codes."
            ),
        ],

        "Java": [
            "Produce a complete Java program.",
            (
                "Use a public class named Main so the generated "
                "source can be compiled consistently."
            ),
            "Read benchmark data only from standard input.",
            "Write only the expected result to standard output.",
        ],

        "Python": [
            "Produce a complete Python 3 program.",
            "Read benchmark data only from standard input.",
            "Write only the expected result to standard output.",
            "Do not require third-party packages.",
        ],

        "JavaScript": [
            "Produce a complete Node.js program.",
            (
                "Prefer synchronous whole-stdin parsing using "
                "fs.readFileSync(0, 'utf8') instead of interactive "
                "readline callbacks."
            ),
            "Parse numeric tokens explicitly as numbers.",
            "Write only the expected result to standard output.",
        ],

        "Go": [
            "Produce a complete Go program using package main.",
            "Provide func main().",
            "Read benchmark data from standard input.",
            "Write only the expected result to standard output.",
        ],

        "Rust": [
            "Produce a complete Rust program with fn main().",
            "Use only the Rust standard library.",
            "Read benchmark data from standard input.",
            "Write only the expected result to standard output.",
        ],

        "C#": [
            "Produce a complete C# program.",
            "Read benchmark data from standard input.",
            "Write only the expected result to standard output.",
            "Do not require external NuGet packages.",
        ],

        "Kotlin": [
            "Produce a complete Kotlin/JVM program.",
            "Provide a valid main entry point.",
            "Read benchmark data from standard input.",
            "Write only the expected result to standard output.",
        ],

        "PHP": [
            "Produce a complete PHP CLI program.",
            "Read benchmark data from standard input.",
            "Write only the expected result to standard output.",
            "Do not require external packages.",
        ],
    }

    rules = requirements.get(
        target_language,
        [
            (
                f"Produce a complete executable "
                f"{target_language} program."
            ),
            "Read benchmark data only from standard input.",
            "Write only the expected result to standard output.",
        ],
    )

    return "\n".join(
        f"- {rule}"
        for rule in rules
    )


# ============================================================
# BENCHMARK REQUIREMENTS
# ============================================================

def _get_benchmark_requirements() -> str:
    rules = [
        (
            "The supplied stdin is the only benchmark workload. "
            "Do not generate random input inside the target program."
        ),
        (
            "Do not hard-code sample input, expected output, "
            "benchmark results, or reference output."
        ),
        (
            "Do not print prompts, labels, explanations, timing "
            "information, debug messages, or diagnostic text."
        ),
        (
            "Do not add artificial delays, sleeps, busy waits, "
            "or unrelated computation."
        ),
        (
            "Do not add internal benchmarking, profiling, timing, "
            "CPU measurement, memory measurement, or energy "
            "measurement code."
        ),
        (
            "The target must perform the benchmarked computation "
            "itself."
        ),
        (
            "The program must terminate normally after producing "
            "the required output."
        ),
        (
            "The generated implementation must follow the exact "
            "stdin contract supplied below."
        ),
    ]

    return "\n".join(
        f"- {rule}"
        for rule in rules
    )

def build_generation_prompt(
    *,
    reference_code: str,
    reference_language: str,
    target_language: str,
    benchmark_name: str,
    description: str | None,
    input_contract: dict[str, Any] | None,
    benchmark_metadata: dict[str, Any] | None = None,
    workload_type: str | None = None,
    resolved_workload: dict[str, Any] | None = None,
    example_input: str | None = None,
    expected_output: str | None = None,
) -> str:
    """
    Build a compact semantic translation prompt.

    The reference source is the primary authority.
    Only essential algorithm, input-contract, and
    target-language constraints are sent to the model.
    """

    reference_language = _normalize_language_name(
        reference_language
    )

    target_language = _normalize_language_name(
        target_language
    )

    algorithm = _extract_algorithm_metadata(
        benchmark_metadata=benchmark_metadata,
        resolved_workload=resolved_workload,
    )

    algorithm_name = (
        algorithm.get("name")
        or algorithm.get("algorithm_name")
        or "unknown"
    )

    algorithm_requirements = (
        _get_algorithm_preservation_requirements(
            algorithm
        )
    )

    language_requirements = (
        _get_language_requirements(
            target_language
        )
    )

    input_contract_text = (
        _format_json_for_prompt(
            input_contract
        )
    )

    return f"""
Convert the following {reference_language} program to
{target_language} for a programming-language benchmark.

Requirements:
- Preserve exactly the same algorithm and observable behavior.
- Preserve the same stdin and stdout behavior.
- Preserve the algorithmic strategy, control flow, early
  termination, ordering, and mutation behavior where relevant.
- Do not replace the core algorithm with built-in search,
  sorting, hashing, lookup, or equivalent library operations.
- Do not generate random input inside the target program.
- Do not hard-code input or expected output.
- Do not add prompts, explanations, timing, profiling,
  debug output, artificial delays, or unrelated computation.
- Read the benchmark workload from standard input.
- Write only the expected program result to standard output.
- Return only complete raw {target_language} source code.
- Do not use Markdown code fences.

Detected algorithm:
{algorithm_name}

Algorithm-specific requirements:
{algorithm_requirements}

Verified stdin contract:
{input_contract_text}

Target-language requirements:
{language_requirements}

Reference {reference_language} code:

{reference_code.strip()}
""".strip()

# ============================================================
# OLLAMA PROVIDER
# ============================================================

def _call_ollama(
    prompt: str,
) -> str:
    """
    Call the local Ollama HTTP API.

    This provider-specific function is intentionally isolated so
    the generation backend can later be replaced by vLLM or
    another self-hosted inference service without changing the
    benchmark engine.
    """

    if not OLLAMA_MODEL:
        raise RuntimeError(
            "OLLAMA_CODE_MODEL is not configured."
        )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.0,
            "num_predict": OLLAMA_NUM_PREDICT,
            "num_ctx": OLLAMA_NUM_CTX,
        },
    }

    request_data = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        url=f"{OLLAMA_BASE_URL}/api/generate",
        data=request_data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=OLLAMA_TIMEOUT_SECONDS,
        ) as response:
            response_body = response.read().decode(
                "utf-8"
            )

    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read().decode(
                "utf-8",
                errors="replace",
            )
        except Exception:
            error_body = ""

        raise RuntimeError(
            "Ollama returned HTTP "
            f"{exc.code}: "
            f"{error_body or exc.reason}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Unable to connect to the local Ollama "
            f"service at {OLLAMA_BASE_URL}. "
            "Ensure Ollama is running."
        ) from exc

    except TimeoutError as exc:
        raise RuntimeError(
            "Ollama code generation timed out."
        ) from exc

    try:
        parsed = json.loads(
            response_body
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Ollama returned an invalid JSON response."
        ) from exc

    if parsed.get("error"):
        raise RuntimeError(
            f"Ollama generation failed: "
            f"{parsed['error']}"
        )

    generated_text = parsed.get(
        "response"
    )

    if not isinstance(
        generated_text,
        str,
    ):
        raise RuntimeError(
            "Ollama response did not contain "
            "generated source code."
        )

    return generated_text


# ============================================================
# RESPONSE CLEANING
# ============================================================

def _strip_markdown_fences(
    text: str,
) -> str:
    """
    Qwen may return Markdown fences even when explicitly told
    not to. Extract the source safely before downstream compile.
    """

    value = str(text or "").strip()

    if not value:
        return ""

    fenced_blocks = re.findall(
        r"```(?:[A-Za-z0-9_+#.\-]*)\s*\n?"
        r"(.*?)```",
        value,
        flags=re.DOTALL,
    )

    if fenced_blocks:
        # A code-generation response should contain one primary
        # source block. Prefer the largest fenced block if the
        # model unexpectedly emits additional tiny examples.
        value = max(
            fenced_blocks,
            key=len,
        ).strip()

    value = re.sub(
        r"^\s*```[A-Za-z0-9_+#.\-]*\s*",
        "",
        value,
    )

    value = re.sub(
        r"\s*```\s*$",
        "",
        value,
    )

    return value.strip()


def _remove_common_model_preamble(
    code: str,
) -> str:
    """
    Remove a very small set of obvious prose prefixes.

    This deliberately avoids aggressive source rewriting.
    Compile/run verification remains responsible for rejecting
    malformed generation.
    """

    value = code.strip()

    prefixes = [
        "Here is the code:",
        "Here is the source code:",
        "Here is the implementation:",
        "Sure, here is the code:",
        "Sure, here's the code:",
    ]

    lowered = value.lower()

    for prefix in prefixes:
        if lowered.startswith(
            prefix.lower()
        ):
            value = value[
                len(prefix):
            ].lstrip()
            break

    return value.strip()


def sanitize_generated_code(
    generated_text: str,
) -> str:
    code = _strip_markdown_fences(
        generated_text
    )

    code = _remove_common_model_preamble(
        code
    )

    return code.strip()


# ============================================================
# BASIC GENERATION VALIDATION
# ============================================================

def _validate_generated_source(
    code: str,
    target_language: str,
) -> None:
    """
    Lightweight generation-level validation only.

    Compilation and execution validation belong to
    custom_benchmark_engine.py.
    """

    if not code:
        raise ValueError(
            "The model returned empty target source code."
        )

    if "```" in code:
        raise ValueError(
            "Generated target source still contains "
            "Markdown code fences."
        )

    if len(code) < 10:
        raise ValueError(
            "Generated target source is unexpectedly short."
        )

    normalized_target = (
        _normalize_language_name(
            target_language
        )
    )

    obvious_markers = {
        "C": [
            "main(",
        ],
        "C++": [
            "main(",
        ],
        "Java": [
            "class ",
            "static void main",
        ],
        "Python": [],
        "JavaScript": [],
        "Go": [
            "package main",
            "func main",
        ],
        "Rust": [
            "fn main",
        ],
        "C#": [
            "class ",
        ],
        "Kotlin": [
            "fun main",
        ],
        "PHP": [
            "<?php",
        ],
    }

    markers = obvious_markers.get(
        normalized_target,
        [],
    )

    if markers and not all(
        marker.lower() in code.lower()
        for marker in markers
    ):
        raise ValueError(
            "Generated source does not contain the expected "
            f"{normalized_target} program structure."
        )


# ============================================================
# PUBLIC GENERATION API
# ============================================================

def generate_target_code(
    *,
    reference_code: str,
    reference_language: str,
    target_language: str,
    benchmark_name: str,
    description: str | None = None,
    input_contract: dict[str, Any] | None = None,
    benchmark_metadata: dict[str, Any] | None = None,
    workload_type: str | None = None,
    resolved_workload: dict[str, Any] | None = None,
    example_input: str | None = None,
    expected_output: str | None = None,
) -> dict[str, Any]:
    """
    Generate one target-language implementation.

    This function does NOT:
        - compile source code,
        - execute source code,
        - measure metrics,
        - verify output equivalence,
        - calculate Green Score.

    Those responsibilities remain in the benchmark pipeline.
    """

    normalized_reference_language = (
        _normalize_language_name(
            reference_language
        )
    )

    normalized_target_language = (
        _normalize_language_name(
            target_language
        )
    )

    if not isinstance(
        reference_code,
        str,
    ) or not reference_code.strip():
        return {
            "status": "generation_error",
            "language": normalized_target_language,
            "code": None,
            "error": (
                "Reference source code is empty."
            ),
        }

    if (
        normalized_reference_language
        not in SUPPORTED_LANGUAGES
    ):
        return {
            "status": "generation_error",
            "language": normalized_target_language,
            "code": None,
            "error": (
                "Unsupported reference language: "
                f"{reference_language}"
            ),
        }

    if (
        normalized_target_language
        not in SUPPORTED_LANGUAGES
    ):
        return {
            "status": "generation_error",
            "language": normalized_target_language,
            "code": None,
            "error": (
                "Unsupported target language: "
                f"{target_language}"
            ),
        }

    if (
        normalized_reference_language
        == normalized_target_language
    ):
        return {
            "status": "generation_error",
            "language": normalized_target_language,
            "code": None,
            "error": (
                "Reference and target languages "
                "must be different."
            ),
        }

    if not isinstance(
        input_contract,
        dict,
    ):
        return {
            "status": "generation_error",
            "language": normalized_target_language,
            "code": None,
            "error": (
                "A verified Input Contract is required "
                "for target-code generation."
            ),
        }

    try:
        prompt = build_generation_prompt(
            reference_code=reference_code,
            reference_language=(
                normalized_reference_language
            ),
            target_language=(
                normalized_target_language
            ),
            benchmark_name=benchmark_name,
            description=description,
            input_contract=input_contract,
            benchmark_metadata=(
                benchmark_metadata
            ),
            workload_type=workload_type,
            resolved_workload=(
                resolved_workload
            ),
            example_input=example_input,
            expected_output=expected_output,
        )

        raw_response = _call_ollama(
            prompt
        )

        generated_code = (
            sanitize_generated_code(
                raw_response
            )
        )

        _validate_generated_source(
            code=generated_code,
            target_language=(
                normalized_target_language
            ),
        )

        return {
            "status": "success",
            "language": (
                normalized_target_language
            ),
            "code": generated_code,
            "error": None,
            "provider": "ollama",
            "model": OLLAMA_MODEL,
        }

    except Exception as exc:
        return {
            "status": "generation_error",
            "language": (
                normalized_target_language
            ),
            "code": None,
            "error": str(exc),
            "provider": "ollama",
            "model": OLLAMA_MODEL,
        }