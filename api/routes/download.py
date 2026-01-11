from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from core.constants import DATA_DIR

router = APIRouter(
    prefix="/jobs/{job_id}/download",
    tags=["download"]
)


@router.get("")
def download_cleaned(job_id: str):
    path = f"{DATA_DIR}/cleaned/{job_id}.csv"

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Cleaned file not found")

    return FileResponse(
        path,
        media_type="text/csv",
        filename=f"{job_id}_cleaned.csv"
    )
