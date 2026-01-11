import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session

from storage.db.repository import JobRepository, ProfilingRepository
from core.constants import DATA_DIR


class ProfilingService:
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
        self.profile_repo = ProfilingRepository(db)

    def run(self, job_id: str):
        try:
            job = self.job_repo.get(job_id)
            if not job:
                raise ValueError("Job not found")

            file_path = Path(DATA_DIR) / f"{job_id}.csv"
            df = pd.read_csv(file_path)

            self.profile_repo.delete_by_job_id(job_id)

            self.profile_repo.create(
                job_id=job_id,
                row_count=len(df),
                column_count=len(df.columns),
                column_types=df.dtypes.astype(str).to_dict(),
                null_counts=df.isnull().sum().to_dict(),
            )

            self.job_repo.update_status(job_id, "suggesting")

        except Exception:
            self.job_repo.update_status(job_id, "failed")
            raise
