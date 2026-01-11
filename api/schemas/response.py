from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from .domain import Job, JobStatus


class CreateJobResponse(BaseModel):
    job: Job


class JobListResponse(BaseModel):
    jobs: List[Job]


class ProfilingResponse(BaseModel):
    job_id: str
    row_count: int
    column_count: int
    column_types: Dict[str, str]
    null_counts: Dict[str, int]


class SuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
