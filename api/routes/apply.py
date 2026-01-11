from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import os

from api.deps import get_db
from services.apply_service import ApplyService
from storage.db.repository import JobRepository
from services.job_service import can_transition
from services.transform_service import apply_transformations
from core.constants import DATA_DIR


router = APIRouter(
    prefix="/jobs/{job_id}/apply",
    tags=["apply"]
)


@router.post("", status_code=202)
def apply_transformations(
    job_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = ApplyService(db)
    bg.add_task(service.run, job_id)
    return {"job_id": job_id, "status": "applying"}


@router.post("")
def apply_cleaning(job_id: str, db: Session = Depends(get_db)):
    job_repo = JobRepository(db)
    job = job_repo.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not can_transition(job.status, "applying"):
        raise HTTPException(status_code=400, detail="Invalid job state")

    input_path = f"{DATA_DIR}/{job.stored_filename}"
    output_dir = f"{DATA_DIR}/cleaned"
    output_path = f"{output_dir}/{job.id}.csv"

    if not os.path.exists(input_path):
        job_repo.update_status(job_id, "failed")
        raise HTTPException(status_code=400, detail="Original file missing")

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path)

    # 🔒 For now, suggestions are read from MCP output already applied
    # We assume suggestions were validated earlier
    suggestions = job.suggestions or []

    cleaned_df = apply_transformations(df, suggestions)
    cleaned_df.to_csv(output_path, index=False)

    job_repo.update_status(job_id, "done")

    return {
        "job_id": job_id,
        "cleaned_file": f"/jobs/{job_id}/download"
    }
