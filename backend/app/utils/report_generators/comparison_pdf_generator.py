from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

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


def _format_float(value, decimals=2) -> str:
    if value is None:
        return "Not available"

    return f"{value:.{decimals}f}"


def generate_comparison_pdf(
    report: ComparisonReportDTO,
) -> bytes:
    """
    Generate a PDF comparison report from stored benchmark results.

    This function does not execute benchmarks or modify database data.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"Green Code Analyzer - Comparison {report.comparison_id}",
        author="Green Code Analyzer",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ComparisonTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "ComparisonSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#526174"),
        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "ComparisonSection",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0B6B2B"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "ComparisonNormal",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
    )

    small_style = ParagraphStyle(
        "ComparisonSmall",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#526174"),
    )

    story = []

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "GREEN CODE ANALYZER",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Implementation Comparison Report",
            subtitle_style,
        )
    )

    # ---------------------------------------------------------
    # COMPARISON INFORMATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Comparison Information",
            section_style,
        )
    )

    comparison_data = [
        ["Comparison ID", str(report.comparison_id)],
        ["Benchmark Task", report.benchmark_name],
        ["Category", _format_optional(report.category)],
        ["Benchmark Size", _format_optional(report.bench_size)],
        ["Input Size", _format_optional(report.input_size)],
        ["Workload Type", _format_optional(report.workload_type)],
        ["Created At", _format_datetime(report.created_at)],
        ["Implementations", str(len(report.results))],
    ]

    comparison_table = Table(
        comparison_data,
        colWidths=[48 * mm, 125 * mm],
    )

    comparison_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF6EC"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#0F172A"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (1, 0),
                    (1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#DDE7DF"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(comparison_table)
    story.append(Spacer(1, 8))

    # ---------------------------------------------------------
    # IMPLEMENTATION RESULTS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Implementation Results",
            section_style,
        )
    )

    result_header = [
        "Language",
        "Execution Time (ms)",
        "CPU (%)",
        "Memory (MB)",
        "Energy (J)",
        "Green Score",
        "Verified",
    ]

    result_rows = [result_header]

    for result in report.results:
        result_rows.append(
            [
                result.language,
                _format_float(result.execution_time, 2),
                _format_float(result.cpu_usage, 2),
                _format_float(result.memory_usage, 2),
                (
                    _format_float(
                        result.energy_consumption,
                        4,
                    )
                    if result.energy_consumption is not None
                    else "Not available"
                ),
                (
                    _format_float(
                        result.green_score,
                        2,
                    )
                    if result.green_score is not None
                    else "Not available"
                ),
                _format_boolean(result.output_verified),
            ]
        )

    results_table = Table(
        result_rows,
        repeatRows=1,
        colWidths=[
            24 * mm,
            28 * mm,
            20 * mm,
            24 * mm,
            23 * mm,
            25 * mm,
            20 * mm,
        ],
    )

    results_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B6B2B"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7.5,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#DDE7DF"),
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (0, -1),
                    "LEFT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F7FBF8"),
                    ],
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(results_table)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # VALIDATION DETAILS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Validation",
            section_style,
        )
    )

    validation_rows = [
        [
            "Language",
            "Analysis ID",
            "Input Size",
            "Verified",
        ]
    ]

    for result in report.results:
        validation_rows.append(
            [
                result.language,
                str(result.analysis_id),
                _format_optional(result.input_size),
                _format_boolean(result.output_verified),
            ]
        )

    validation_table = Table(
        validation_rows,
        repeatRows=1,
        colWidths=[
            45 * mm,
            35 * mm,
            45 * mm,
            45 * mm,
        ],
    )

    validation_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#EAF6EC"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#DDE7DF"),
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(validation_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # NOTE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Note:</b> This comparison report is generated "
            "from stored benchmark analysis results. Generating "
            "the report does not rerun the benchmark.",
            small_style,
        )
    )

    story.append(
        Paragraph(
            "Energy values represent measured energy consumption "
            "during the stored benchmark execution. No Energy "
            "Saved value is calculated in this report.",
            small_style,
        )
    )

    document.build(story)

    return buffer.getvalue()