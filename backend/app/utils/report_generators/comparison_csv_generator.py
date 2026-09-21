import csv
from io import StringIO

from app.schemas.report import ComparisonReportDTO


def _format_datetime(value) -> str:
    if value is None:
        return "Not available"

    return value.strftime("%d %b %Y, %H:%M:%S")


def _format_optional(value) -> str:
    if value is None or value == "":
        return "Not available"

    return str(value)


def _format_boolean(value) -> str:
    if value is True:
        return "Yes"

    if value is False:
        return "No"

    return "Not available"


def generate_comparison_csv(
    report: ComparisonReportDTO,
) -> bytes:
    """
    Generate a CSV comparison report from stored results.

    No benchmark execution is performed.
    """

    buffer = StringIO(newline="")
    writer = csv.writer(buffer)

    # ---------------------------------------------------------
    # Report Information
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Comparison Report",
            "",
        ]
    )

    writer.writerow(
        [
            "Comparison ID",
            report.comparison_id,
        ]
    )

    writer.writerow(
        [
            "Benchmark Task",
            report.benchmark_name,
        ]
    )

    writer.writerow(
        [
            "Category",
            _format_optional(report.category),
        ]
    )

    writer.writerow(
        [
            "Benchmark Size",
            _format_optional(report.bench_size),
        ]
    )

    writer.writerow(
        [
            "Input Size",
            _format_optional(report.input_size),
        ]
    )

    writer.writerow(
        [
            "Workload Type",
            _format_optional(report.workload_type),
        ]
    )

    writer.writerow(
        [
            "Created At",
            _format_datetime(report.created_at),
        ]
    )

    writer.writerow(
        [
            "Implementations",
            len(report.results),
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # Implementation Results
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Implementation Results",
        ]
    )

    writer.writerow(
        [
            "Language",
            "Compiler",
            "Version",
            "Analysis ID",
            "Execution Time (ms)",
            "CPU Usage (%)",
            "Memory Usage (MB)",
            "Energy Consumption (J)",
            "Green Score",
            "Green Score Label",
            "Output Verified",
        ]
    )

    for result in report.results:
        writer.writerow(
            [
                result.language,
                result.compiler or "Not available",
                result.version or "Not available",
                result.analysis_id,
                (
                    f"{result.execution_time:.2f}"
                    if result.execution_time is not None
                    else "Not available"
                ),
                (
                    f"{result.cpu_usage:.2f}"
                    if result.cpu_usage is not None
                    else "Not available"
                ),
                (
                    f"{result.memory_usage:.2f}"
                    if result.memory_usage is not None
                    else "Not available"
                ),
                (
                    f"{result.energy_consumption:.4f}"
                    if result.energy_consumption is not None
                    else "Not available"
                ),
                (
                    f"{result.green_score:.2f}"
                    if result.green_score is not None
                    else "Not available"
                ),
                result.green_score_label or "Not available",
                _format_boolean(result.output_verified),
            ]
        )

    writer.writerow([])

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Validation",
        ]
    )

    writer.writerow(
        [
            "Language",
            "Analysis ID",
            "Input Size",
            "Benchmark Size",
            "Output Verified",
        ]
    )

    for result in report.results:
        writer.writerow(
            [
                result.language,
                result.analysis_id,
                _format_optional(result.input_size),
                _format_optional(result.bench_size),
                _format_boolean(result.output_verified),
            ]
        )

    writer.writerow([])

    # ---------------------------------------------------------
    # Note
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Note",
            (
                "This comparison report is generated from stored "
                "benchmark analysis results. Generating the report "
                "does not rerun the benchmark."
            ),
        ]
    )

    writer.writerow(
        [
            "Energy Note",
            (
                "Energy values represent measured energy "
                "consumption during the stored benchmark execution."
            ),
        ]
    )

    return buffer.getvalue().encode("utf-8-sig")