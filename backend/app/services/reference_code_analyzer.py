import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from app.services.compiler_runner import validate_syntax


SUPPORTED_LANGUAGES = [
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
]


LANGUAGE_MAP = {
    "C": "c",
    "C++": "cpp",
    "Java": "java",
    "Python": "python",
    "JavaScript": "javascript",
    "Go": "go",
    "Rust": "rust",
    "C#": "csharp",
    "Kotlin": "kotlin",
    "PHP": "php",
}


EXTENSION_MAP = {
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


STRONG_DETECTION_SCORE = 7
MIN_DETECTION_SCORE = 2
AMBIGUITY_MARGIN = 2


def _clean_code(reference_code: str) -> str:
    if not isinstance(reference_code, str):
        return ""

    return (
        reference_code
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def _score_languages(code: str) -> dict[str, int]:
    lowered = code.lower()

    scores = {
        language: 0
        for language in SUPPORTED_LANGUAGES
    }

    # --------------------------------------------------
    # PHP
    # --------------------------------------------------
    if re.search(r"<\?php\b", lowered):
        scores["PHP"] += 15

    if re.search(r"\$\w+", code):
        scores["PHP"] += 4

    if re.search(r"\becho\s+", lowered):
        scores["PHP"] += 4

    if re.search(r"\bfunction\s+\w+\s*\(", lowered):
        scores["PHP"] += 1

    if re.search(r"\brequire(?:_once)?\s*\(", lowered):
        scores["PHP"] += 3

    if re.search(r"\binclude(?:_once)?\s*\(", lowered):
        scores["PHP"] += 3

    # --------------------------------------------------
    # C#
    # --------------------------------------------------
    if re.search(r"\busing\s+system\s*;", lowered):
        scores["C#"] += 10

    if re.search(r"\bconsole\.writeline\s*\(", lowered):
        scores["C#"] += 8

    if re.search(r"\bconsole\.readline\s*\(", lowered):
        scores["C#"] += 5

    if re.search(
        r"\bnamespace\s+[a-z_]\w*(?:\.[a-z_]\w*)*\s*",
        lowered,
    ):
        scores["C#"] += 4

    if re.search(
        r"\b(public|private|protected|internal)\s+(static\s+)?"
        r"(class|interface|struct|enum)\b",
        lowered,
    ):
        scores["C#"] += 3

    if re.search(
        r"\b(bool|string|double|decimal|object)\s+\w+",
        lowered,
    ):
        scores["C#"] += 2

    # --------------------------------------------------
    # Java
    # --------------------------------------------------
    if re.search(
        r"\bpublic\s+static\s+void\s+main\s*\(",
        code,
    ):
        scores["Java"] += 10

    if re.search(r"\bsystem\.out\.(print|println|printf)\s*\(", lowered):
        scores["Java"] += 8

    if re.search(r"\bsystem\.in\b", lowered):
        scores["Java"] += 4

    if re.search(
        r"\bimport\s+java\.[a-z0-9_.]+\s*;",
        code,
        re.IGNORECASE,
    ):
        scores["Java"] += 8

    if re.search(
        r"\bpublic\s+class\s+\w+",
        code,
    ):
        scores["Java"] += 5

    if re.search(
        r"\b(public|private|protected)\s+"
        r"(static\s+)?"
        r"(int|long|double|float|boolean|String|char)\s+\w+",
        code,
    ):
        scores["Java"] += 2

    if re.search(
        r"\bnew\s+[A-Z]\w*\s*\(",
        code,
    ):
        scores["Java"] += 1

    # --------------------------------------------------
    # Kotlin
    # --------------------------------------------------
    if re.search(
        r"\bfun\s+main\s*\(",
        code,
    ):
        scores["Kotlin"] += 10

    if re.search(
        r"\bfun\s+\w+\s*\(",
        code,
    ):
        scores["Kotlin"] += 5

    if re.search(
        r"\b(val|var)\s+\w+\s*:",
        code,
    ):
        scores["Kotlin"] += 5

    if re.search(
        r"\b(val|var)\s+\w+\s*=",
        code,
    ):
        scores["Kotlin"] += 2

    if re.search(r"\bprintln\s*\(", lowered):
        scores["Kotlin"] += 3

    if re.search(r"\breadline\s*\(\s*\)", lowered):
        scores["Kotlin"] += 4

    if re.search(r"\bimport\s+kotlin\.", lowered):
        scores["Kotlin"] += 6

    if re.search(r"\bwhen\s*\(", lowered):
        scores["Kotlin"] += 2

    # --------------------------------------------------
    # Go
    # --------------------------------------------------
    if re.search(
        r"\bpackage\s+main\b",
        code,
    ):
        scores["Go"] += 12

    if re.search(
        r"\bfunc\s+main\s*\(",
        code,
    ):
        scores["Go"] += 10

    if re.search(
        r"\bfunc\s+\w+\s*\(",
        code,
    ):
        scores["Go"] += 3

    if re.search(r"\bfmt\.(scan|scanln|scanf|fscan|println|printf)\s*\(", lowered):
        scores["Go"] += 7

    if re.search(r"\b:=\s*", code):
        scores["Go"] += 4

    if re.search(r"\bpackage\s+\w+", lowered):
        scores["Go"] += 3

    if re.search(r"\bgo\s+\w+\s*\(", lowered):
        scores["Go"] += 2

    if re.search(r"\bdefer\s+\w+\s*\(", lowered):
        scores["Go"] += 2

    # --------------------------------------------------
    # Rust
    # --------------------------------------------------
    if re.search(
        r"\bfn\s+main\s*\(",
        code,
    ):
        scores["Rust"] += 12

    if re.search(
        r"\bfn\s+\w+\s*\(",
        code,
    ):
        scores["Rust"] += 5

    if "println!" in lowered:
        scores["Rust"] += 7

    if re.search(r"\bstd::io\b", lowered):
        scores["Rust"] += 6

    if re.search(r"\blet\s+mut\b", code):
        scores["Rust"] += 5

    if re.search(r"\blet\s+\w+\s*:", code):
        scores["Rust"] += 3

    if re.search(r"\buse\s+std::", lowered):
        scores["Rust"] += 6

    if re.search(r"\bmatch\s+\w+\s*\{", lowered):
        scores["Rust"] += 3

    if re.search(r"->\s*[A-Za-z_][A-Za-z0-9_:<>]*", code):
        scores["Rust"] += 2

    # --------------------------------------------------
    # Python
    # --------------------------------------------------
    if re.search(
        r"^\s*def\s+\w+\s*\(",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 9

    if re.search(
        r"^\s*class\s+\w+\s*(\(|:)",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 6

    if re.search(
        r"\bprint\s*\(",
        code,
    ):
        scores["Python"] += 5

    if re.search(
        r"\binput\s*\(",
        code,
    ):
        scores["Python"] += 4

    if "__name__" in code:
        scores["Python"] += 7

    if re.search(
        r"^\s*(from\s+\w+(?:\.\w+)*\s+import|import\s+\w+)",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 4

    if re.search(
        r"\b(True|False|None)\b",
        code,
    ):
        scores["Python"] += 3

    if re.search(
        r"\b(range|len|str|int|float|list|dict|set)\s*\(",
        code,
    ):
        scores["Python"] += 2

    if re.search(
        r"^\s*for\s+\w+\s+in\s+",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 3

    if re.search(
        r"^\s*if\s+.+:\s*$",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 3

    if re.search(
        r"^\s*(elif|else|try|except|finally|with)\b.*:\s*$",
        code,
        re.MULTILINE,
    ):
        scores["Python"] += 2

    # --------------------------------------------------
    # JavaScript
    # --------------------------------------------------
    if re.search(
        r"\bconsole\.log\s*\(",
        lowered,
    ):
        scores["JavaScript"] += 8

    if re.search(
        r"\bconsole\.error\s*\(",
        lowered,
    ):
        scores["JavaScript"] += 5

    if re.search(
        r"\bprocess\.stdin\b",
        lowered,
    ):
        scores["JavaScript"] += 7

    if re.search(
        r"\breadfilesync\s*\(\s*0",
        lowered,
    ):
        scores["JavaScript"] += 8

    if re.search(
        r"\brequire\s*\(\s*['\"]",
        lowered,
    ):
        scores["JavaScript"] += 5

    if re.search(
        r"\b(const|let|var)\s+\w+",
        code,
    ):
        scores["JavaScript"] += 3

    if "=>" in code:
        scores["JavaScript"] += 5

    if re.search(
        r"\bfunction\s+\w+\s*\(",
        code,
    ):
        scores["JavaScript"] += 3

    if re.search(
        r"\b(import|export)\s+.*\bfrom\s+['\"]",
        code,
    ):
        scores["JavaScript"] += 5

    if re.search(
        r"\bundefined\b",
        lowered,
    ):
        scores["JavaScript"] += 2

    # --------------------------------------------------
    # C++
    # --------------------------------------------------
    if re.search(
        r"#\s*include\s*<iostream>",
        lowered,
    ):
        scores["C++"] += 10

    if re.search(
        r"#\s*include\s*<vector>",
        lowered,
    ):
        scores["C++"] += 7

    if re.search(
        r"#\s*include\s*<algorithm>",
        lowered,
    ):
        scores["C++"] += 7

    if re.search(
        r"#\s*include\s*<bits/stdc\+\+\.h>",
        lowered,
    ):
        scores["C++"] += 10

    if re.search(
        r"\bstd::",
        lowered,
    ):
        scores["C++"] += 6

    if re.search(
        r"\b(cin|cout|cerr)\s*(>>|<<)",
        code,
    ):
        scores["C++"] += 7

    if re.search(
        r"\bvector\s*<",
        code,
    ):
        scores["C++"] += 7

    if re.search(
        r"\busing\s+namespace\s+std\b",
        lowered,
    ):
        scores["C++"] += 6

    if re.search(
        r"\bstring\s+\w+\s*;",
        code,
    ):
        scores["C++"] += 2

    if re.search(
        r"\bauto\s+\w+\s*=",
        code,
    ):
        scores["C++"] += 2

    # --------------------------------------------------
    # C
    # --------------------------------------------------
    if re.search(
        r"#\s*include\s*<stdio\.h>",
        lowered,
    ):
        scores["C"] += 10

    if re.search(
        r"#\s*include\s*<stdlib\.h>",
        lowered,
    ):
        scores["C"] += 6

    if re.search(
        r"#\s*include\s*<string\.h>",
        lowered,
    ):
        scores["C"] += 6

    if re.search(
        r"#\s*include\s*<stdbool\.h>",
        lowered,
    ):
        scores["C"] += 5

    if re.search(
        r"\bprintf\s*\(",
        code,
    ):
        scores["C"] += 7

    if re.search(
        r"\bscanf\s*\(",
        code,
    ):
        scores["C"] += 6

    if re.search(
        r"\bmalloc\s*\(",
        code,
    ):
        scores["C"] += 5

    if re.search(
        r"\bcalloc\s*\(",
        code,
    ):
        scores["C"] += 4

    if re.search(
        r"\brealloc\s*\(",
        code,
    ):
        scores["C"] += 4

    if re.search(
        r"\bfree\s*\(",
        code,
    ):
        scores["C"] += 4

    # --------------------------------------------------
    # Generic C/C++ evidence
    # --------------------------------------------------
    if re.search(
        r"\bint\s+main\s*\(",
        code,
    ):
        scores["C"] += 2
        scores["C++"] += 2

    # --------------------------------------------------
    # Explicit C++-only evidence
    # --------------------------------------------------
    if re.search(
        r"\b(class|template)\s*<|"
        r"\bclass\s+\w+\s*\{",
        code,
    ):
        scores["C++"] += 2

    if re.search(
        r"\bnew\s+\w+(\s*<[^;{}]+>)?\s*\(",
        code,
    ):
        scores["C++"] += 2

    return scores


def _rank_candidates(scores: dict[str, int]) -> list[dict[str, Any]]:
    ranked = sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return [
        {
            "language": language,
            "score": score,
        }
        for language, score in ranked
        if score > 0
    ]


def _candidate_confidence(
    ranked_candidates: list[dict[str, Any]],
) -> float:
    if not ranked_candidates:
        return 0.0

    best_score = ranked_candidates[0]["score"]

    if len(ranked_candidates) == 1:
        return 0.99 if best_score >= MIN_DETECTION_SCORE else 0.50

    second_score = ranked_candidates[1]["score"]

    if best_score <= 0:
        return 0.0

    margin = max(0, best_score - second_score)

    confidence = 0.50 + (
        margin / max(best_score, 1)
    ) * 0.40

    if best_score >= STRONG_DETECTION_SCORE:
        confidence += 0.05

    if best_score >= 12:
        confidence += 0.02

    return round(
        min(confidence, 0.99),
        3,
    )


def _is_strong_detection(
    ranked_candidates: list[dict[str, Any]],
) -> bool:
    if not ranked_candidates:
        return False

    best_score = ranked_candidates[0]["score"]

    if best_score < STRONG_DETECTION_SCORE:
        return False

    if len(ranked_candidates) == 1:
        return True

    second_score = ranked_candidates[1]["score"]

    return (
        best_score - second_score
        >= AMBIGUITY_MARGIN
    )


def _validate_candidate_language(
    reference_code: str,
    language: str,
) -> dict[str, Any]:
    internal_language = LANGUAGE_MAP[language]
    extension = EXTENSION_MAP[internal_language]

    temp_dir = tempfile.mkdtemp(
        prefix="greencode_language_check_"
    )

    try:
        source_file = (
            Path(temp_dir) / f"source{extension}"
        )

        source_file.write_text(
            reference_code,
            encoding="utf-8",
        )

        result = validate_syntax(
            language=internal_language,
            source_file=str(source_file),
            output_dir=temp_dir,
        )

        syntax_valid = bool(
            result.get("syntax_valid", False)
        )

        return {
            "language": language,
            "syntax_valid": syntax_valid,
            "syntax_errors": result.get(
                "syntax_errors",
                [],
            ),
            "validation_confidence": (
                1.0 if syntax_valid else 0.0
            ),
        }

    except Exception as exc:
        return {
            "language": language,
            "syntax_valid": False,
            "syntax_errors": [str(exc)],
            "validation_confidence": 0.0,
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )


def detect_reference_language(
    reference_code: str,
) -> dict[str, Any]:
    code = _clean_code(reference_code)

    if not code:
        return {
            "language": None,
            "confidence": 0.0,
            "reason": "Reference code is empty.",
            "detection_status": "empty",
            "candidates": [],
        }

    scores = _score_languages(code)

    ranked_candidates = _rank_candidates(scores)

    if not ranked_candidates:
        return {
            "language": None,
            "confidence": 0.0,
            "reason": (
                "No supported programming-language "
                "signature was identified."
            ),
            "detection_status": "weak",
            "candidates": [],
        }

    best_language = ranked_candidates[0]["language"]
    best_score = ranked_candidates[0]["score"]

    confidence = _candidate_confidence(
        ranked_candidates
    )

    if best_score < MIN_DETECTION_SCORE:
        detection_status = "weak"
    elif _is_strong_detection(ranked_candidates):
        detection_status = "strong"
    else:
        detection_status = "ambiguous"

    return {
        "language": best_language,
        "confidence": confidence,
        "reason": (
            "Language detected from deterministic "
            "source-code signatures."
        ),
        "detection_status": detection_status,
        "candidates": ranked_candidates[:10],
    }


def _resolve_language_with_validation(
    reference_code: str,
    detection_result: dict[str, Any],
) -> dict[str, Any]:
    candidates = detection_result.get(
        "candidates",
        [],
    )

    if not candidates:
        return {
            **detection_result,
            "language": None,
            "confidence": 0.0,
            "detection_status": "unresolved",
            "reason": (
                "No language candidates were available "
                "for syntax validation."
            ),
        }

    candidate_languages = [
        candidate["language"]
        for candidate in candidates
        if candidate.get("score", 0) >= MIN_DETECTION_SCORE
    ]

    if not candidate_languages:
        return {
            **detection_result,
            "language": None,
            "confidence": 0.0,
            "detection_status": "unresolved",
            "reason": (
                "Language signatures were too weak "
                "to resolve safely."
            ),
            "validation_candidates": [],
        }

    validation_results = []

    for language in candidate_languages:
        validation_results.append(
            _validate_candidate_language(
                reference_code,
                language,
            )
        )

    valid_candidates = [
        result
        for result in validation_results
        if result["syntax_valid"]
    ]

    if not valid_candidates:
        return {
            **detection_result,
            "language": None,
            "confidence": 0.0,
            "reason": (
                "Language signatures were weak or ambiguous "
                "and none of the candidate languages passed "
                "syntax validation."
            ),
            "detection_status": "unresolved",
            "validation_candidates": validation_results,
        }

    candidate_scores = {
        candidate["language"]: candidate["score"]
        for candidate in candidates
    }

    valid_candidates.sort(
        key=lambda result: (
            -candidate_scores.get(
                result["language"],
                0,
            ),
            -result.get(
                "validation_confidence",
                0.0,
            ),
            result["language"],
        )
    )

    selected = valid_candidates[0]

    signature_score = candidate_scores.get(
        selected["language"],
        0,
    )

    if signature_score >= STRONG_DETECTION_SCORE:
        final_confidence = max(
            detection_result.get(
                "confidence",
                0.0,
            ),
            0.90,
        )
    elif signature_score >= MIN_DETECTION_SCORE:
        final_confidence = max(
            detection_result.get(
                "confidence",
                0.0,
            ),
            0.75,
        )
    else:
        final_confidence = 0.70

    return {
        **detection_result,
        "language": selected["language"],
        "confidence": round(
            min(final_confidence, 0.99),
            3,
        ),
        "reason": (
            "Language resolved using deterministic "
            "source-code signatures and syntax validation."
        ),
        "detection_status": "validated",
        "validation_candidates": validation_results,
    }


def analyze_reference_code(
    reference_code: str,
) -> dict[str, Any]:
    code = _clean_code(reference_code)

    if not code:
        return {
            "language": None,
            "confidence": 0.0,
            "syntax_valid": False,
            "syntax_errors": [
                "Reference code is empty."
            ],
            "reason": "Reference code is empty.",
            "detection_status": "empty",
            "candidates": [],
        }

    language_result = detect_reference_language(
        code
    )

    detection_status = language_result.get(
        "detection_status"
    )

    if detection_status in {
        "weak",
        "ambiguous",
    }:
        language_result = _resolve_language_with_validation(
            code,
            language_result,
        )

    language = language_result.get(
        "language"
    )

    if language is None:
        return {
            "language": None,
            "confidence": language_result.get(
                "confidence",
                0.0,
            ),
            "syntax_valid": False,
            "syntax_errors": language_result.get(
                "validation_candidates",
                [],
            ),
            "reason": language_result.get(
                "reason",
                "Unable to determine the programming language.",
            ),
            "detection_status": language_result.get(
                "detection_status",
                "unresolved",
            ),
            "candidates": language_result.get(
                "candidates",
                [],
            ),
            "validation_candidates": language_result.get(
                "validation_candidates",
                [],
            ),
        }

    internal_language = LANGUAGE_MAP[language]
    extension = EXTENSION_MAP[internal_language]

    temp_dir = tempfile.mkdtemp(
        prefix="greencode_reference_"
    )

    try:
        source_file = (
            Path(temp_dir) / f"source{extension}"
        )

        source_file.write_text(
            code,
            encoding="utf-8",
        )

        syntax_result = validate_syntax(
            language=internal_language,
            source_file=str(source_file),
            output_dir=temp_dir,
        )

        syntax_valid = bool(
            syntax_result.get(
                "syntax_valid",
                False,
            )
        )

        return {
            "language": language,
            "confidence": language_result.get(
                "confidence",
                0.0,
            ),
            "syntax_valid": syntax_valid,
            "syntax_errors": syntax_result.get(
                "syntax_errors",
                [],
            ),
            "reason": language_result.get(
                "reason"
            ),
            "detection_status": language_result.get(
                "detection_status"
            ),
            "candidates": language_result.get(
                "candidates",
                [],
            ),
            "validation_candidates": language_result.get(
                "validation_candidates",
                [],
            ),
        }

    except Exception as exc:
        return {
            "language": language,
            "confidence": language_result.get(
                "confidence",
                0.0,
            ),
            "syntax_valid": False,
            "syntax_errors": [str(exc)],
            "reason": (
                "Language was detected, but final "
                "syntax validation failed."
            ),
            "detection_status": language_result.get(
                "detection_status"
            ),
            "candidates": language_result.get(
                "candidates",
                [],
            ),
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )