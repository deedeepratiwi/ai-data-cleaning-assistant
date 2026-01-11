from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(
    prefix="/jobs",
    tags=["orchestration"]
)

N8N_WEBHOOK_URL = "http://n8n:5678/webhook/run-job"


@router.post("/{job_id}/run")
def run_job(job_id: str):
    try:
        response = httpx.post(
            N8N_WEBHOOK_URL,
            json={"job_id": job_id},
            timeout=5
        )
        response.raise_for_status()
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to trigger workflow")

    return {"status": "workflow_started", "job_id": job_id}
