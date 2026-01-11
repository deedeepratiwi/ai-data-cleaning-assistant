from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from pathlib import Path

from api.deps import get_db
from storage.db.models import JobModel
from storage.db.repository import JobRepository
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
