# """Deterministic benchmark metadata intelligence.

# This module is intentionally *not* an algorithm detector and does not inspect
# source code. It combines two authoritative, already-computed intelligence
# results:

# * Algorithm Intelligence -> computational identity
# * Input Contract Analyzer -> input structure

# The output is presentation metadata with explicit provenance and confidence.
# Generation is deterministic and schema-versioned so the same intelligence
# inputs always produce the same metadata.
# """
# from __future__ import annotations

# from typing import Any

# SCHEMA_VERSION = 1
# GENERATION_VERSION = 1

# _CONFIDENCE_LEVELS = ((0.90, "high"), (0.70, "medium"))

# _ALGORITHM_LABELS = {
#     "binary-search": "Binary Search",
#     "linear-search": "Linear Search",
#     "merge-sort": "Merge Sort",
#     "quick-sort": "Quick Sort",
#     "heap-sort": "Heap Sort",
#     "bubble-sort": "Bubble Sort",
#     "insertion-sort": "Insertion Sort",
#     "selection-sort": "Selection Sort",
#     "sorting": "Sorting",
#     "two-pointers": "Two Pointers",
#     "sliding-window": "Sliding Window",
#     "prefix-sum": "Prefix Sum",
#     "graph-traversal": "Graph Traversal",
#     "graph-algorithm": "Graph Algorithm",
#     "tree-traversal": "Tree Traversal",
#     "dynamic-programming": "Dynamic Programming",
#     "greedy": "Greedy Algorithm",
#     "backtracking": "Backtracking",
#     "recursion": "Recursion",
#     "hashing": "Hashing",
#     "string-processing": "String Processing",
#     "matrix-processing": "Matrix Processing",
#     "stack": "Stack Processing",
#     "queue": "Queue Processing",
# }

# _FAMILY_LABELS = {
#     "searching": "Searching",
#     "sorting": "Sorting",
#     "two-pointers": "Two Pointers",
#     "sliding-window": "Sliding Window",
#     "graph-traversal": "Graph Traversal",
#     "graph-algorithm": "Graph Algorithms",
#     "tree-traversal": "Tree Traversal",
#     "dynamic-programming": "Dynamic Programming",
#     "greedy": "Greedy",
#     "backtracking": "Backtracking",
#     "recursion": "Recursion",
#     "hashing": "Hashing",
#     "string-processing": "String Processing",
#     "matrix-processing": "Matrix Processing",
#     "prefix-sum": "Prefix Sum",
#     "stack": "Stack",
#     "queue": "Queue",
# }

# _INPUT_LABELS = {
#     "numeric-array": "Integer Array",
#     "integer-array": "Integer Array",
#     "array-plus-target": "Integer Array + Target",
#     "array-target": "Integer Array + Target",
#     "text": "Text Input",
#     "string": "String Input",
#     "string-line": "String Input",
#     "string-array": "String Array",
#     "matrix": "Integer Matrix",
#     "matrix-plus-target": "Integer Matrix + Target",
#     "graph": "Graph",
#     "weighted-graph": "Weighted Graph",
#     "graph-with-source": "Graph + Source",
#     "weighted-graph-with-source": "Weighted Graph + Source",
#     "tree": "Tree",
#     "linked-list": "Linked List",
#     "multiple-test-cases": "Multiple Test Cases",
#     "test-cases": "Multiple Test Cases",
#     "stack": "Stack",
#     "stack-input": "Stack",
#     "queue": "Queue",
#     "queue-input": "Queue",
#     "pairs": "Pairs",
#     "tuples": "Tuples",
#     "pairs-tuples": "Pairs / Tuples",
#     "key-value": "Key-Value Records",
#     "key-value-data": "Key-Value Records",
#     "key-value-records": "Key-Value Records",
#     "mixed-records": "Mixed Records",
#     "mixed-datatype-records": "Mixed Records",
#     "float-array": "Floating-Point Array",
#     "character-array": "Character Array",
#     "characters": "Character Input",
#     "boolean-array": "Boolean Array",
#     "bool-array": "Boolean Array",
#     "boolean": "Boolean Input",
#     "date": "Date Input",
#     "datetime": "Date-Time Input",
#     "date-time": "Date-Time Input",
#     "timestamp": "Timestamp Input",
#     "url": "URL Collection",
#     "html": "HTML Collection",
#     "json": "JSON Records",
#     "csv": "CSV Records",
#     "eof-stream": "EOF Stream",
#     "eof-records": "EOF Records",
#     "sentinel-stream": "Sentinel Stream",
#     "sentinel-records": "Sentinel Records",
#     "queries": "Queries",
#     "query-stream": "Query Stream",
#     "range-queries": "Range Queries",
# }

# _DESCRIPTION_TEMPLATES = {
#     "binary-search": "Benchmarks binary search over {input} using a target value.",
#     "linear-search": "Benchmarks linear search over {input} to locate a target value.",
#     "merge-sort": "Benchmarks merge sort over {input}.",
#     "quick-sort": "Benchmarks quicksort over {input}.",
#     "heap-sort": "Benchmarks heap sort over {input}.",
#     "bubble-sort": "Benchmarks bubble sort over {input}.",
#     "insertion-sort": "Benchmarks insertion sort over {input}.",
#     "selection-sort": "Benchmarks selection sort over {input}.",
#     "sorting": "Benchmarks sorting operations over {input}.",
#     "two-pointers": "Benchmarks a two-pointer algorithm over {input}.",
#     "sliding-window": "Benchmarks a sliding-window algorithm over {input}.",
#     "prefix-sum": "Benchmarks prefix-sum processing over {input}.",
#     "graph-traversal": "Benchmarks graph traversal over {input}.",
#     "graph-algorithm": "Benchmarks a graph algorithm over {input}.",
#     "tree-traversal": "Benchmarks tree traversal over {input}.",
#     "dynamic-programming": "Benchmarks dynamic-programming processing over {input}.",
#     "greedy": "Benchmarks a greedy algorithm over {input}.",
#     "backtracking": "Benchmarks backtracking over {input}.",
#     "recursion": "Benchmarks a recursive algorithm over {input}.",
#     "hashing": "Benchmarks hash-based processing over {input}.",
#     "string-processing": "Benchmarks string processing over {input}.",
#     "matrix-processing": "Benchmarks matrix processing over {input}.",
#     "stack": "Benchmarks stack-based processing over {input}.",
#     "queue": "Benchmarks queue-based processing over {input}.",
# }


# def _normalize_key(value: Any) -> str | None:
#     if value is None:
#         return None
#     value = str(value).strip().lower().replace("_", "-").replace(" ", "-")
#     return value or None


# def _clamp_score(value: Any) -> float:
#     try:
#         score = float(value)
#     except (TypeError, ValueError):
#         return 0.0
#     return round(max(0.0, min(1.0, score)), 2)


# def _confidence_level(score: float) -> str:
#     for threshold, level in _CONFIDENCE_LEVELS:
#         if score >= threshold:
#             return level
#     return "low"


# def _as_evidence(value: Any) -> list[str]:
#     if value is None:
#         return []
#     if isinstance(value, (list, tuple, set)):
#         return [str(item) for item in value if str(item).strip()]
#     if isinstance(value, dict):
#         # Preserve useful structured evidence without inventing a summary.
#         return [f"{key}: {value[key]}" for key in sorted(value)]
#     return [str(value)]


# def _extract_algorithm(algorithm: dict[str, Any] | None) -> dict[str, Any]:
#     data = algorithm or {}
#     name = _normalize_key(data.get("algorithm_name") or data.get("name"))
#     family = _normalize_key(data.get("algorithm_family") or data.get("family"))
#     specificity = str(data.get("specificity") or "unknown")
#     confidence = _clamp_score(data.get("confidence", 0.0))
#     evidence = _as_evidence(data.get("evidence") or data.get("reason"))
#     known = bool(name and name not in {"custom", "unknown"})
#     return {
#         "name": name,
#         "family": family,
#         "specificity": specificity,
#         "confidence": confidence,
#         "evidence": evidence,
#         "known": known,
#     }


# def _extract_input(input_structure: dict[str, Any] | None) -> dict[str, Any]:
#     data = input_structure or {}
#     contract = data.get("contract") or data.get("input_contract") or {}
#     detection = data.get("detection") or {}
#     workload_type = _normalize_key(
#         data.get("workload_type") or data.get("contract_type") or contract.get("contract_type")
#     )
#     confidence = _clamp_score(
#         contract.get("confidence", detection.get("confidence", data.get("confidence", 0.0)))
#     )
#     evidence = _as_evidence(detection.get("reason") or data.get("reason"))
#     known = bool(workload_type and workload_type not in {"custom", "unknown"})
#     return {
#         "workload_type": workload_type,
#         "confidence": confidence,
#         "evidence": evidence,
#         "known": known,
#     }


# def _label_algorithm(name: str | None, family: str | None) -> str | None:
#     if name and name not in {"custom", "unknown"}:
#         return _ALGORITHM_LABELS.get(name, name.replace("-", " ").title())
#     if family and family not in {"custom", "unknown"}:
#         return _FAMILY_LABELS.get(family, family.replace("-", " ").title())
#     return None


# def _label_input(workload_type: str | None) -> str | None:
#     if not workload_type:
#         return None
#     return _INPUT_LABELS.get(workload_type, workload_type.replace("-", " ").title())


# def _description(algorithm_name: str | None, input_label: str | None, algorithm_label: str | None) -> str:
#     input_phrase = (input_label or "the benchmark input").lower()
#     if algorithm_name in _DESCRIPTION_TEMPLATES:
#         return _DESCRIPTION_TEMPLATES[algorithm_name].format(input=input_phrase)
#     if algorithm_label:
#         return f"Benchmarks {algorithm_label.lower()} over {input_phrase}."
#     return f"Benchmarks processing of {input_phrase} workload."


# def generate_benchmark_metadata(
#     *,
#     input_structure: dict[str, Any] | None,
#     algorithm: dict[str, Any] | None,
# ) -> dict[str, Any]:
#     """Generate deterministic, provenance-rich benchmark metadata."""
#     algo = _extract_algorithm(algorithm)
#     inp = _extract_input(input_structure)

#     algorithm_label = _label_algorithm(algo["name"], algo["family"])
#     input_label = _label_input(inp["workload_type"])

#     # If both signals exist, the weaker authoritative signal bounds confidence.
#     # Missing/unknown signals deliberately produce low confidence rather than
#     # pretending that a partial inference is fully reliable.
#     score = _clamp_score(min(algo["confidence"], inp["confidence"]))

#     if algo["known"] and inp["known"] and algorithm_label and input_label:
#         name = f"{algorithm_label} — {input_label}"
#         category = _FAMILY_LABELS.get(
#             algo["family"] or "",
#             (algo["family"] or "custom").replace("-", " ").title(),
#         )
#         description = _description(algo["name"], input_label, algorithm_label)
#         inference_status = "reliable" if score >= 0.90 else "limited"
#         inference_message = "Automatically generated from Algorithm Intelligence and Input Contract."
#     elif algo["known"] and algorithm_label:
#         name = algorithm_label
#         category = _FAMILY_LABELS.get(
#             algo["family"] or "",
#             (algo["family"] or "custom").replace("-", " ").title(),
#         )
#         description = _description(algo["name"], input_label, algorithm_label)
#         inference_status = "limited"
#         inference_message = "Algorithm identified automatically; input structure is not fully verified."
#     elif inp["known"] and input_label:
#         name = f"{input_label} Workload"
#         category = "Custom"
#         description = f"Benchmarks processing of {input_label.lower()} workload."
#         inference_status = "limited"
#         inference_message = "The algorithm could not be identified reliably."
#     else:
#         name = "Custom Benchmark Workload"
#         category = "Custom"
#         description = "Benchmarks the supplied reference implementation using a custom workload."
#         inference_status = "limited"
#         inference_message = "Neither a reliable algorithm nor a verified input structure was identified."

#     return {
#         "name": name,
#         "category": category,
#         "description": description,
#         "source": "automatic",
#         "confidence": {
#             "score": score,
#             "level": _confidence_level(score),
#         },
#         "provenance": {
#             "algorithm": {
#                 "source": "algorithm_intelligence",
#                 "name": algo["name"],
#                 "family": algo["family"],
#                 "specificity": algo["specificity"],
#                 "confidence": algo["confidence"],
#                 "evidence": algo["evidence"],
#             },
#             "input": {
#                 "source": "input_contract_analyzer",
#                 "workload_type": inp["workload_type"],
#                 "confidence": inp["confidence"],
#                 "evidence": inp["evidence"],
#             },
#         },
#         "generation": {
#             "strategy": "deterministic-template",
#             "version": GENERATION_VERSION,
#         },
#         "inference": {
#             "status": inference_status,
#             "message": inference_message,
#         },
#         "schema_version": SCHEMA_VERSION,
#     }


"""Deterministic benchmark metadata intelligence.

This module is intentionally *not* an algorithm detector and does not inspect
source code. It combines two authoritative, already-computed intelligence
results:

* Algorithm Intelligence -> computational identity
* Input Contract Analyzer -> input structure

The output is presentation metadata with explicit provenance and confidence.
Generation is deterministic and schema-versioned so the same intelligence
inputs always produce the same metadata.
"""
from __future__ import annotations

from typing import Any

SCHEMA_VERSION = 1
GENERATION_VERSION = 1

_CONFIDENCE_LEVELS = ((0.90, "high"), (0.70, "medium"))

_ALGORITHM_LABELS = {
    "binary-search": "Binary Search",
    "linear-search": "Linear Search",
    "merge-sort": "Merge Sort",
    "quick-sort": "Quick Sort",
    "heap-sort": "Heap Sort",
    "bubble-sort": "Bubble Sort",
    "insertion-sort": "Insertion Sort",
    "selection-sort": "Selection Sort",
    "sorting": "Sorting",
    "two-pointers": "Two Pointers",
    "sliding-window": "Sliding Window",
    "prefix-sum": "Prefix Sum",
    "graph-traversal": "Graph Traversal",
    "graph-algorithm": "Graph Algorithm",
    "tree-traversal": "Tree Traversal",
    "dynamic-programming": "Dynamic Programming",
    "greedy": "Greedy Algorithm",
    "backtracking": "Backtracking",
    "recursion": "Recursion",
    "hashing": "Hashing",
    "string-processing": "String Processing",
    "matrix-processing": "Matrix Processing",
    "stack": "Stack Processing",
    "queue": "Queue Processing",
}

_FAMILY_LABELS = {
    "searching": "Searching",
    "sorting": "Sorting",
    "two-pointers": "Two Pointers",
    "sliding-window": "Sliding Window",
    "graph-traversal": "Graph Traversal",
    "graph-algorithm": "Graph Algorithms",
    "tree-traversal": "Tree Traversal",
    "dynamic-programming": "Dynamic Programming",
    "greedy": "Greedy",
    "backtracking": "Backtracking",
    "recursion": "Recursion",
    "hashing": "Hashing",
    "string-processing": "String Processing",
    "matrix-processing": "Matrix Processing",
    "prefix-sum": "Prefix Sum",
    "stack": "Stack",
    "queue": "Queue",
}

_INPUT_LABELS = {
    "numeric-array": "Integer Array",
    "integer-array": "Integer Array",
    "array-plus-target": "Integer Array + Target",
    "array-target": "Integer Array + Target",
    "text": "Text Input",
    "string": "String Input",
    "string-line": "String Input",
    "string-array": "String Array",
    "matrix": "Integer Matrix",
    "matrix-plus-target": "Integer Matrix + Target",
    "graph": "Graph",
    "weighted-graph": "Weighted Graph",
    "graph-with-source": "Graph + Source",
    "weighted-graph-with-source": "Weighted Graph + Source",
    "tree": "Tree",
    "linked-list": "Linked List",
    "multiple-test-cases": "Multiple Test Cases",
    "test-cases": "Multiple Test Cases",
    "stack": "Stack",
    "stack-input": "Stack",
    "queue": "Queue",
    "queue-input": "Queue",
    "pairs": "Pairs",
    "tuples": "Tuples",
    "pairs-tuples": "Pairs / Tuples",
    "key-value": "Key-Value Records",
    "key-value-data": "Key-Value Records",
    "key-value-records": "Key-Value Records",
    "mixed-records": "Mixed Records",
    "mixed-datatype-records": "Mixed Records",
    "float-array": "Floating-Point Array",
    "character-array": "Character Array",
    "characters": "Character Input",
    "boolean-array": "Boolean Array",
    "bool-array": "Boolean Array",
    "boolean": "Boolean Input",
    "date": "Date Input",
    "datetime": "Date-Time Input",
    "date-time": "Date-Time Input",
    "timestamp": "Timestamp Input",
    "url": "URL Collection",
    "html": "HTML Collection",
    "json": "JSON Records",
    "csv": "CSV Records",
    "eof-stream": "EOF Stream",
    "eof-records": "EOF Records",
    "sentinel-stream": "Sentinel Stream",
    "sentinel-records": "Sentinel Records",
    "queries": "Queries",
    "query-stream": "Query Stream",
    "range-queries": "Range Queries",
}

_DESCRIPTION_TEMPLATES = {
    "binary-search": "Benchmarks binary search over {input} using a target value.",
    "linear-search": "Benchmarks linear search over {input} to locate a target value.",
    "merge-sort": "Benchmarks merge sort over {input}.",
    "quick-sort": "Benchmarks quicksort over {input}.",
    "heap-sort": "Benchmarks heap sort over {input}.",
    "bubble-sort": "Benchmarks bubble sort over {input}.",
    "insertion-sort": "Benchmarks insertion sort over {input}.",
    "selection-sort": "Benchmarks selection sort over {input}.",
    "sorting": "Benchmarks sorting operations over {input}.",
    "two-pointers": "Benchmarks a two-pointer algorithm over {input}.",
    "sliding-window": "Benchmarks a sliding-window algorithm over {input}.",
    "prefix-sum": "Benchmarks prefix-sum processing over {input}.",
    "graph-traversal": "Benchmarks graph traversal over {input}.",
    "graph-algorithm": "Benchmarks a graph algorithm over {input}.",
    "tree-traversal": "Benchmarks tree traversal over {input}.",
    "dynamic-programming": "Benchmarks dynamic-programming processing over {input}.",
    "greedy": "Benchmarks a greedy algorithm over {input}.",
    "backtracking": "Benchmarks backtracking over {input}.",
    "recursion": "Benchmarks a recursive algorithm over {input}.",
    "hashing": "Benchmarks hash-based processing over {input}.",
    "string-processing": "Benchmarks string processing over {input}.",
    "matrix-processing": "Benchmarks matrix processing over {input}.",
    "stack": "Benchmarks stack-based processing over {input}.",
    "queue": "Benchmarks queue-based processing over {input}.",
}


def _normalize_key(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip().lower().replace("_", "-").replace(" ", "-")
    return value or None


def _clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return round(max(0.0, min(1.0, score)), 2)


def _confidence_level(score: float) -> str:
    for threshold, level in _CONFIDENCE_LEVELS:
        if score >= threshold:
            return level
    return "low"


def _as_evidence(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        # Preserve useful structured evidence without inventing a summary.
        return [f"{key}: {value[key]}" for key in sorted(value)]
    return [str(value)]


def _extract_algorithm(algorithm: dict[str, Any] | None) -> dict[str, Any]:
    data = algorithm or {}
    name = _normalize_key(data.get("algorithm_name") or data.get("name"))
    family = _normalize_key(data.get("algorithm_family") or data.get("family"))
    specificity = str(data.get("specificity") or "unknown")
    confidence = _clamp_score(data.get("confidence", 0.0))
    evidence = _as_evidence(data.get("evidence") or data.get("reason"))
    known = bool(name and name not in {"custom", "unknown"})
    return {
        "name": name,
        "family": family,
        "specificity": specificity,
        "confidence": confidence,
        "evidence": evidence,
        "known": known,
    }


def _extract_input(input_structure: dict[str, Any] | None) -> dict[str, Any]:
    data = input_structure or {}
    contract = data.get("contract") or data.get("input_contract") or {}
    detection = data.get("detection") or {}
    workload_type = _normalize_key(
        data.get("workload_type") or data.get("contract_type") or contract.get("contract_type")
    )
    confidence = _clamp_score(
        contract.get("confidence", detection.get("confidence", data.get("confidence", 0.0)))
    )
    evidence = _as_evidence(detection.get("reason") or data.get("reason"))
    known = bool(workload_type and workload_type not in {"custom", "unknown"})
    return {
        "workload_type": workload_type,
        "confidence": confidence,
        "evidence": evidence,
        "known": known,
    }


def _label_algorithm(name: str | None, family: str | None) -> str | None:
    if name and name not in {"custom", "unknown"}:
        return _ALGORITHM_LABELS.get(name, name.replace("-", " ").title())
    if family and family not in {"custom", "unknown"}:
        return _FAMILY_LABELS.get(family, family.replace("-", " ").title())
    return None


def _label_input(workload_type: str | None) -> str | None:
    if not workload_type:
        return None
    return _INPUT_LABELS.get(workload_type, workload_type.replace("-", " ").title())


def _description(algorithm_name: str | None, input_label: str | None, algorithm_label: str | None) -> str:
    input_phrase = (input_label or "the benchmark input").lower()
    if algorithm_name in _DESCRIPTION_TEMPLATES:
        return _DESCRIPTION_TEMPLATES[algorithm_name].format(input=input_phrase)
    if algorithm_label:
        return f"Benchmarks {algorithm_label.lower()} over {input_phrase}."
    return f"Benchmarks processing of {input_phrase} workload."


def generate_benchmark_metadata(
    *,
    input_structure: dict[str, Any] | None,
    algorithm: dict[str, Any] | None,
) -> dict[str, Any]:
    """Generate deterministic, provenance-rich benchmark metadata."""
    algo = _extract_algorithm(algorithm)
    inp = _extract_input(input_structure)

    algorithm_label = _label_algorithm(algo["name"], algo["family"])
    input_label = _label_input(inp["workload_type"])

    # If both signals exist, the weaker authoritative signal bounds confidence.
    # Missing/unknown signals deliberately produce low confidence rather than
    # pretending that a partial inference is fully reliable.
    score = _clamp_score(min(algo["confidence"], inp["confidence"]))

    if algo["known"] and inp["known"] and algorithm_label and input_label:
        name = f"{algorithm_label} — {input_label}"
        category = _FAMILY_LABELS.get(
            algo["family"] or "",
            (algo["family"] or "custom").replace("-", " ").title(),
        )
        description = _description(algo["name"], input_label, algorithm_label)
        inference_status = "reliable" if score >= 0.90 else "limited"
        inference_message = "Automatically generated from Algorithm Intelligence and Input Contract."
    elif algo["known"] and algorithm_label:
        name = algorithm_label
        category = _FAMILY_LABELS.get(
            algo["family"] or "",
            (algo["family"] or "custom").replace("-", " ").title(),
        )
        description = _description(algo["name"], input_label, algorithm_label)
        inference_status = "limited"
        inference_message = "Algorithm identified automatically; input structure is not fully verified."
    elif inp["known"] and input_label:
        name = f"{input_label} Workload"
        category = "Custom"
        description = f"Benchmarks processing of {input_label.lower()} workload."
        inference_status = "limited"
        inference_message = "The algorithm could not be identified reliably."
    else:
        name = "Custom Benchmark Workload"
        category = "Custom"
        description = "Benchmarks the supplied reference implementation using a custom workload."
        inference_status = "limited"
        inference_message = "Neither a reliable algorithm nor a verified input structure was identified."

    return {
        "name": name,
        "category": category,
        "description": description,
        "source": "automatic",
        "confidence": {
            "score": score,
            "level": _confidence_level(score),
        },
        "provenance": {
            "algorithm": {
                "source": "algorithm_intelligence",
                "name": algo["name"],
                "family": algo["family"],
                "specificity": algo["specificity"],
                "confidence": algo["confidence"],
                "evidence": algo["evidence"],
            },
            "input": {
                "source": "input_contract_analyzer",
                "workload_type": inp["workload_type"],
                "confidence": inp["confidence"],
                "evidence": inp["evidence"],
            },
        },
        "generation": {
            "strategy": "deterministic-template",
            "version": GENERATION_VERSION,
        },
        "inference": {
            "status": inference_status,
            "message": inference_message,
        },
        "schema_version": SCHEMA_VERSION,
    }
