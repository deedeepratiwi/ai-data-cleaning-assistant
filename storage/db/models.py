from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    profiling = relationship(
        "ProfilingResult",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ProfilingResult(Base):
    __tablename__ = "profiling_results"

    job_id = Column(String, ForeignKey("jobs.id"), primary_key=True)
    row_count = Column(Integer, nullable=False)
    column_count = Column(Integer, nullable=False)
    column_types = Column(JSON, nullable=False)
    null_counts = Column(JSON, nullable=False)

    job = relationship("JobModel", back_populates="profiling")


class SuggestionModel(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)

    suggestions = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobModel")
