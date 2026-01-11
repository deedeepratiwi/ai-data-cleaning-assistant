from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import json

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


@router.get("/dtypes")
def get_dtypes(job_id: str):
    """
    Get dtype information for the cleaned dataset.
    CSV format doesn't preserve data types (especially datetime64).
    Use this endpoint to understand the intended data types.
    
    To read the CSV with proper dtypes:
    ```python
    import pandas as pd
    import requests
    
    # Get dtype info
    dtype_info = requests.get(f"/jobs/{job_id}/download/dtypes").json()
    
    # Read CSV with datetime columns parsed
    df = pd.read_csv(
        f"/jobs/{job_id}/download",
        parse_dates=dtype_info['datetime_columns']
    )
    ```
    """
    metadata_path = f"{DATA_DIR}/cleaned/{job_id}_dtypes.json"

    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Dtype metadata not found")

    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    return JSONResponse(content=metadata)
