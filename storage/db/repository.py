from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from storage.db.models import JobModel, ProfilingResult, SuggestionModel
from core.constants import JOB_STATUS_TRANSITIONS


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: JobModel):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: str):
        return self.db.query(JobModel).filter_by(id=job_id).first()

    def update_status(self, job_id: str, new_status: str):
        job = self.get(job_id)
        if not job:
            raise ValueError("Job not found")

        allowed = JOB_STATUS_TRANSITIONS.get(job.status, [])
        if new_status not in allowed:
            raise ValueError(f"Invalid transition {job.status} → {new_status}")

        job.status = new_status
        self.db.commit()
        self.db.refresh(job)
        return job


class ProfilingRepository:
    def __init__(self, db: Session):
        self.db = db

    def delete_by_job_id(self, job_id: str):
        self.db.query(ProfilingResult).filter(
            ProfilingResult.job_id == job_id
        ).delete()
        self.db.commit()

    def create(
        self,
        job_id: str,
        row_count: int,
        column_count: int,
        column_types: dict,
        null_counts: dict,
    ):
        profiling = ProfilingResult(
            job_id=job_id,
            row_count=row_count,
            column_count=column_count,
            column_types=column_types,
            null_counts=null_counts,
        )

        self.db.add(profiling)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Profiling already exists")

        self.db.refresh(profiling)
        return profiling

    def get_by_job_id(self, job_id: str):
        return (
            self.db.query(ProfilingResult)
            .filter(ProfilingResult.job_id == job_id)
            .one_or_none()
        )


class SuggestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_id: str, suggestions: list[dict]):
        record = SuggestionModel(
            job_id=job_id,
            suggestions=suggestions,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_job_id(self, job_id: str):
        return (
            self.db.query(SuggestionModel)
            .filter(SuggestionModel.job_id == job_id)
            .order_by(SuggestionModel.created_at.desc())
            .first()
        )
