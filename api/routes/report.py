from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from core.constants import DATA_DIR
from services.report_service import ReportService
from api.deps import get_db
from pathlib import Path
import os

router = APIRouter(prefix="/jobs/{job_id}/report", tags=["report"])

@router.get("")
def get_report(job_id: str, db: Session = Depends(get_db)):
    report_dir = Path(DATA_DIR) / "reports"
    report_path = report_dir / f"{job_id}.md"
    if not os.path.exists(report_path):
        # Try to generate if not exists
        report = ReportService(db).generate_report(job_id)
        if report == "No report available.":
            raise HTTPException(404, "Report not found")
        ReportService(db).save_report(job_id, report)
    return FileResponse(str(report_path), media_type="text/markdown", filename=f"{job_id}_report.md")
