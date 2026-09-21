import csv
from io import StringIO

from app.schemas.report import ReportDTO


def _format_datetime(value) -> str:
    return value.strftime(
        "%d %b %Y, %H:%M:%S"
    )


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


def generate_csv(
    report: ReportDTO,
) -> bytes:

    buffer = StringIO(
        newline=""
    )

    writer = csv.writer(buffer)

    # ---------------------------------------------------------
    # REPORT INFORMATION
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Report Field",
            "Value",
        ]
    )

    writer.writerow(
        [
            "Report Title",
            report.report_title,
        ]
    )

    writer.writerow(
        [
            "Analysis ID",
            report.analysis_id,
        ]
    )

    writer.writerow(
        [
            "User ID",
            report.user_id,
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # BENCHMARK INFORMATION
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Benchmark Information",
            "",
        ]
    )

    writer.writerow(
        [
            "Benchmark Task",
            report.metadata.benchmark_task,
        ]
    )

    writer.writerow(
        [
            "Category",
            _format_optional(
                report.metadata.category
            ),
        ]
    )

    writer.writerow(
        [
            "Analysis Type",
            report.metadata.analysis_type.title(),
        ]
    )

    writer.writerow(
        [
            "Language",
            report.metadata.language,
        ]
    )

    writer.writerow(
        [
            "Input Size",
            _format_optional(
                report.metadata.input_size
            ),
        ]
    )

    writer.writerow(
        [
            "Benchmark Size",
            _format_optional(
                report.metadata.bench_size
            ),
        ]
    )

    writer.writerow(
        [
            "Workload Type",
            _format_optional(
                report.metadata.workload_type
            ),
        ]
    )

    writer.writerow(
        [
            "Execution Date",
            _format_datetime(
                report.metadata.execution_date
            ),
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # EXECUTION ENVIRONMENT
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Execution Environment",
            "",
        ]
    )

    writer.writerow(
        [
            "Runtime",
            _format_optional(
                report.metadata.runtime
            ),
        ]
    )

    writer.writerow(
        [
            "Compiler",
            _format_optional(
                report.metadata.compiler
            ),
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # PERFORMANCE METRICS
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Performance Metrics",
            "",
        ]
    )

    writer.writerow(
        [
            "Execution Time (ms)",
            f"{report.metrics.execution_time:.2f}",
        ]
    )

    writer.writerow(
        [
            "CPU Usage (%)",
            f"{report.metrics.cpu_usage:.2f}",
        ]
    )

    writer.writerow(
        [
            "Memory Usage (MB)",
            f"{report.metrics.memory_usage:.2f}",
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # SUSTAINABILITY METRICS
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Sustainability Metrics",
            "",
        ]
    )

    if report.metrics.energy_consumption is not None:
        energy_value = (
            f"{report.metrics.energy_consumption:.4f}"
        )
    else:
        energy_value = "Not available"

    if report.metrics.green_score is not None:
        green_score_value = (
            f"{report.metrics.green_score:.2f}"
        )
    else:
        green_score_value = "Not available"

    writer.writerow(
        [
            "Energy Consumption (J)",
            energy_value,
        ]
    )

    writer.writerow(
        [
            "Green Score",
            green_score_value,
        ]
    )

    writer.writerow(
        [
            "Green Score Label",
            _format_optional(
                report.metrics.green_score_label
            ),
        ]
    )

    writer.writerow([])

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    writer.writerow(
        [
            "Validation",
            "",
        ]
    )

    writer.writerow(
        [
            "Output Verified",
            _format_boolean(
                report.metrics.output_verified
            ),
        ]
    )

    # ---------------------------------------------------------
    # COMPARISON INFORMATION
    # ---------------------------------------------------------

    if report.rank is not None:

        writer.writerow([])

        writer.writerow(
            [
                "Comparison Information",
                "",
            ]
        )

        writer.writerow(
            [
                "Rank",
                report.rank,
            ]
        )

        if report.total_comparisons is not None:
            writer.writerow(
                [
                    "Total Comparisons",
                    report.total_comparisons,
                ]
            )

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    writer.writerow([])

    writer.writerow(
        [
            "Note",
            (
                "This report is generated from stored "
                "benchmark analysis results. Generating "
                "the report does not rerun the benchmark."
            ),
        ]
    )

    return buffer.getvalue().encode(
        "utf-8-sig"
    )