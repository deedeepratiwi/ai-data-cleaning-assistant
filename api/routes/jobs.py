from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path

from api.deps import get_db
from storage.db.models import JobModel
from storage.db.repository import JobRepository, ProfilingRepository
from services.profiling_service import ProfilingService
from core.constants import DATA_DIR

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    job = JobRepository(db).create(
        JobModel(original_filename=file.filename)
    )

    Path(DATA_DIR).mkdir(exist_ok=True)
    with open(Path(DATA_DIR) / f"{job.id}.csv", "wb") as f:
        f.write(file.file.read())

    return {"job_id": job.id, "status": job.status}


@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = JobRepository(db).get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.get("/{job_id}/profile")
def get_profile(job_id: str, db: Session = Depends(get_db)):
    profile = ProfilingRepository(db).get_by_job_id(job_id)
    if not profile:
        raise HTTPException(404, "Profiling not found")
    return profile


@router.post("/{job_id}/profile", status_code=202)
def start_profiling(
    job_id: str,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        JobRepository(db).update_status(job_id, "profiling")
    except ValueError as e:
        raise HTTPException(400, str(e))

    bg.add_task(ProfilingService(db).run, job_id)
    return {"job_id": job_id, "status": "profiling"}


@router.post("/{job_id}/retry", status_code=202)
def retry(job_id: str, bg: BackgroundTasks, db: Session = Depends(get_db)):
    job = JobRepository(db).get(job_id)
    if not job or job.status != "failed":
        raise HTTPException(400, "Job not retryable")

    JobRepository(db).update_status(job_id, "profiling")
    bg.add_task(ProfilingService(db).run, job_id)

    return {"job_id": job_id, "status": "profiling"}
