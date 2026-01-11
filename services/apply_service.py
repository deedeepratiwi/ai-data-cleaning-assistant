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
        job = self.job_repo.get(job_id)
        if not job:
            raise ValueError("Job not found")

        if not can_transition(job.status, "applying"):
            raise ValueError("Invalid job state")

        suggestions = self.suggestion_repo.get_by_job_id(job_id)
        if not suggestions:
            raise ValueError("Suggestions missing")

        input_path = Path(DATA_DIR) / job.input_filename
        output_path = Path(DATA_DIR) / f"{job.id}_cleaned.csv"

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
