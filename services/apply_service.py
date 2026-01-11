import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session

from storage.db.repository import (
    JobRepository,
    SuggestionRepository,
)
from transformations.registry import TRANSFORMATION_REGISTRY
from services.job_service import can_transition
from core.constants import DATA_DIR


class ApplyService:
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
        self.suggestion_repo = SuggestionRepository(db)

    def run(self, job_id: str):
        try:
            job = self.job_repo.get(job_id)
            if not job:
                raise ValueError("Job not found")

            # Allow running if job is in 'applying' status (already set by suggestion)
            # or if it can transition to applying
            if job.status != "applying" and not can_transition(job.status, "applying"):
                raise ValueError("Invalid job state")

            suggestions = self.suggestion_repo.get_by_job_id(job_id)
            if not suggestions:
                raise ValueError("Suggestions missing")

            input_path = Path(DATA_DIR) / f"{job_id}.csv"
            output_dir = Path(DATA_DIR) / "cleaned"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{job_id}.csv"

            df = pd.read_csv(input_path)

            for step in suggestions.suggestions:
                op_name = step.get("operation")
                params = step.get("params", {})

                operation = TRANSFORMATION_REGISTRY.get(op_name)
                if not operation:
                    continue  # silently skip unsupported ops

                df = operation(df, **params)

            df.to_csv(output_path, index=False)

            self.job_repo.update_status(job_id, "done")
        except Exception:
            self.job_repo.update_status(job_id, "failed")
            raise
