from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from storage.db.repository import SuggestionRepository, JobRepository, ProfilingRepository
from services.suggestion_service import SuggestionService
from services.job_service import can_transition


router = APIRouter(
    prefix="/jobs/{job_id}/suggestions",
    tags=["suggestions"]
)


@router.post("", status_code=202)
def start_suggestions(
    job_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = SuggestionService(db, None)
    bg.add_task(service.run, job_id)
    return {"job_id": job_id, "status": "suggesting"}


@router.get("")
def get_suggestions(job_id: str, db: Session = Depends(get_db)):
    repo = SuggestionRepository(db)
    result = repo.get_by_job_id(job_id)

    if not result:
        raise HTTPException(404, "Suggestions not found")

    return {
        "job_id": job_id,
        "suggestions": result.suggestions,
    }
