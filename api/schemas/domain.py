from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JobStatus(str, Enum):
    pending = "pending"
    profiling = "profiling"
    suggesting = "suggesting"
    applying = "applying"
    done = "done"
    failed = "failed"


class Job(BaseModel):
    id: str
    original_filename: str
    status: JobStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes=True

