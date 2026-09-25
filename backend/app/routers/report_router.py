from io import BytesIO

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.report import ReportDTO
from app.services import report_service
from app.services import comparison_report_service
from app.utils.report_generators.pdf_generator import (
    generate_pdf,
)
from app.utils.report_generators.excel_generator import (
    generate_excel,
)
from app.utils.report_generators.csv_generator import (
    generate_csv,
)
from app.utils.report_generators.comparison_pdf_generator import (
    generate_comparison_pdf,
)
from app.utils.report_generators.comparison_excel_generator import (
    generate_comparison_excel,
)
from app.utils.report_generators.comparison_csv_generator import (
    generate_comparison_csv,
)
router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/analysis/{analysis_id}",
    response_model=ReportDTO,
)
def get_report_data(
    analysis_id: int,
    db: Session = Depends(get_db),
):

    report = report_service.get_report_data(
        db=db,
        analysis_id=analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    return report


@router.get(
    "/analysis/{analysis_id}/pdf",
)
def download_pdf_report(
    analysis_id: int,
    db: Session = Depends(get_db),
):

    report = report_service.get_report_data(
        db=db,
        analysis_id=analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    pdf_bytes = generate_pdf(report)

    filename = (
        f"GreenCodeAnalyzer_"
        f"Analysis_{analysis_id}.pdf"
    )

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
        },
    )

@router.get(
    "/analysis/{analysis_id}/xlsx",
)
def download_excel_report(
    analysis_id: int,
    db: Session = Depends(get_db),
):

    report = report_service.get_report_data(
        db=db,
        analysis_id=analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    excel_bytes = generate_excel(report)

    filename = (
        f"GreenCodeAnalyzer_"
        f"Analysis_{analysis_id}.xlsx"
    )

    return StreamingResponse(
        BytesIO(excel_bytes),
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
        },
    )
    
@router.get(
    "/analysis/{analysis_id}/csv",
)

def download_csv_report(
    analysis_id: int,
    db: Session = Depends(get_db),
):

    report = report_service.get_report_data(
        db=db,
        analysis_id=analysis_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    csv_bytes = generate_csv(report)

    filename = (
        f"GreenCodeAnalyzer_"
        f"Analysis_{analysis_id}.csv"
    )

    return StreamingResponse(
        BytesIO(csv_bytes),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
        },
    )


@router.get("/comparison/{comparison_id}/pdf")
def download_comparison_pdf(
    comparison_id: int,
    db: Session = Depends(get_db),
):
    report = comparison_report_service.get_comparison_report_data(
        db=db,
        comparison_id=comparison_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Comparison not found.",
        )

    if not report.results:
        raise HTTPException(
            status_code=400,
            detail="Comparison has no analysis results.",
        )

    pdf_bytes = generate_comparison_pdf(report)

    filename = (
        f"GreenCodeAnalyzer_Comparison_"
        f"{comparison_id}.pdf"
    )

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )


@router.get("/comparison/{comparison_id}/xlsx")
def download_comparison_excel(
    comparison_id: int,
    db: Session = Depends(get_db),
):
    report = comparison_report_service.get_comparison_report_data(
        db=db,
        comparison_id=comparison_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Comparison not found.",
        )

    if not report.results:
        raise HTTPException(
            status_code=400,
            detail="Comparison has no analysis results.",
        )

    excel_bytes = generate_comparison_excel(report)

    filename = (
        f"GreenCodeAnalyzer_Comparison_"
        f"{comparison_id}.xlsx"
    )

    return StreamingResponse(
        BytesIO(excel_bytes),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )


@router.get("/comparison/{comparison_id}/csv")
def download_comparison_csv(
    comparison_id: int,
    db: Session = Depends(get_db),
):
    report = comparison_report_service.get_comparison_report_data(
        db=db,
        comparison_id=comparison_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Comparison not found.",
        )

    if not report.results:
        raise HTTPException(
            status_code=400,
            detail="Comparison has no analysis results.",
        )

    csv_bytes = generate_comparison_csv(report)

    filename = (
        f"GreenCodeAnalyzer_Comparison_"
        f"{comparison_id}.csv"
    )

    return StreamingResponse(
        BytesIO(csv_bytes),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )