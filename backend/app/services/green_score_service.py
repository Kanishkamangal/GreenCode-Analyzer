from typing import List, Dict, Any


# ============================================================
# GREEN SCORE WEIGHTS
# ============================================================

EXECUTION_WEIGHT = 0.25
CPU_WEIGHT = 0.20
MEMORY_WEIGHT = 0.15
ENERGY_WEIGHT = 0.40


# ============================================================
# NORMALIZATION
# Lower raw value = better score
# ============================================================

def normalize_lower_is_better(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    """
    Convert a raw metric into a 0-100 comparative score.

    Lower metric values are considered better.

    Best value  -> 100
    Worst value -> 0

    If all values are identical, every result receives 100
    because no language is worse than another for that metric.
    """

    if maximum == minimum:
        return 100.0

    score = (
        (maximum - value)
        / (maximum - minimum)
    ) * 100

    return max(
        0.0,
        min(100.0, score)
    )


# ============================================================
# GREEN SCORE LABEL
# ============================================================

def get_green_score_label(
    score: float
) -> str:

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Very Good"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Moderate"

    if score >= 20:
        return "Poor"

    return "Very Poor"


# ============================================================
# CALCULATE GREEN SCORES
# ============================================================

def calculate_green_scores(
    results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    """
    Calculate comparative Green Scores for all languages
    participating in one benchmark comparison.

    Green Score =
        25% Execution Score
        20% CPU Score
        15% Memory Score
        40% Energy Score
    """

    if not results:
        return results

    if len(results) < 2:
        for result in results:
            result["green_score"] = None
            result["green_score_label"] = None

        return results
    # --------------------------------------------------------
    # Energy is mandatory for the professional Green Score.
    # --------------------------------------------------------

    if any(
        result.get("energy_consumption") is None
        for result in results
    ):

        for result in results:
            result["green_score"] = None
            result["green_score_label"] = None

        return results

    # --------------------------------------------------------
    # Extract raw metric values
    # --------------------------------------------------------

    execution_values = [
        float(result["execution_time"])
        for result in results
    ]

    cpu_values = [
        float(result["cpu_usage"])
        for result in results
    ]

    memory_values = [
        float(result["memory_usage"])
        for result in results
    ]

    energy_values = [
        float(result["energy_consumption"])
        for result in results
    ]

    # --------------------------------------------------------
    # Find comparison boundaries
    # --------------------------------------------------------

    min_execution = min(execution_values)
    max_execution = max(execution_values)

    min_cpu = min(cpu_values)
    max_cpu = max(cpu_values)

    min_memory = min(memory_values)
    max_memory = max(memory_values)

    min_energy = min(energy_values)
    max_energy = max(energy_values)

    # --------------------------------------------------------
    # Calculate each language score
    # --------------------------------------------------------

    for result in results:

        execution_score = normalize_lower_is_better(
            float(result["execution_time"]),
            min_execution,
            max_execution,
        )

        cpu_score = normalize_lower_is_better(
            float(result["cpu_usage"]),
            min_cpu,
            max_cpu,
        )

        memory_score = normalize_lower_is_better(
            float(result["memory_usage"]),
            min_memory,
            max_memory,
        )

        energy_score = normalize_lower_is_better(
            float(result["energy_consumption"]),
            min_energy,
            max_energy,
        )

        green_score = (
            EXECUTION_WEIGHT * execution_score
            + CPU_WEIGHT * cpu_score
            + MEMORY_WEIGHT * memory_score
            + ENERGY_WEIGHT * energy_score
        )

        green_score = round(
            green_score,
            2
        )

        result["execution_score"] = round(
            execution_score,
            2
        )

        result["cpu_score"] = round(
            cpu_score,
            2
        )

        result["memory_score"] = round(
            memory_score,
            2
        )

        result["energy_score"] = round(
            energy_score,
            2
        )

        result["green_score"] = green_score

        result["green_score_label"] = (
            get_green_score_label(
                green_score
            )
        )

    return results