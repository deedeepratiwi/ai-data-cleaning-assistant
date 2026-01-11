from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from storage.db.repository import SuggestionRepository
from services.suggestion_service import generate_suggestions, SuggestionService
from services.job_service import can_transition

# placeholder LLM client
from agents.mcp_client import get_llm_client


router = APIRouter(
    prefix="/jobs/{job_id}/suggestions",
    tags=["suggestions"]
)


@router.post("", status_code=202)
def generate_suggestions(
    job_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = SuggestionService(db, get_llm_client())
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


@router.post("")
def run_suggestions(job_id: str, db: Session = Depends(get_db)):
    job_repo = JobRepository(db)
    profile_repo = ProfilingRepository(db)

    job = job_repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not can_transition(job.status, "suggesting"):
        raise HTTPException(status_code=400, detail="Invalid job state")

    profiling = profile_repo.get_by_job_id(job_id)
    if not profiling:
        raise HTTPException(status_code=404, detail="Profiling not found")

    suggestions = generate_suggestions(
        profiling_result={
            "row_count": profiling.row_count,
            "column_stats": profiling.column_stats,
        }
    )

    job_repo.update_status(job_id, "applying")

    return {
        "job_id": job_id,
        "suggestions": suggestions,
    }
