from sqlalchemy.orm import Session

from storage.db.repository import (
    JobRepository,
    ProfilingRepository,
    SuggestionRepository,
)
from agents.data_cleaning_agent import DataCleaningAgent
from services.job_service import can_transition

from agents.mcp_client import MCPClient


class SuggestionService:
    def __init__(self, db: Session, llm_client):
        self.db = db
        self.job_repo = JobRepository(db)
        self.profile_repo = ProfilingRepository(db)
        self.suggestion_repo = SuggestionRepository(db)
        self.agent = DataCleaningAgent(llm_client)

    def run(self, job_id: str):
        job = self.job_repo.get(job_id)
        if not job:
            raise ValueError("Job not found")

        if not can_transition(job.status, "suggesting"):
            raise ValueError("Invalid job state")

        profiling = self.profile_repo.get_by_job_id(job_id)
        if not profiling:
            raise ValueError("Profiling missing")

        suggestions = self.agent.suggest(
            {
                "row_count": profiling.row_count,
                "column_count": profiling.column_count,
                "column_types": profiling.column_types,
                "null_counts": profiling.null_counts,
            }
        )

        self.suggestion_repo.create(job_id, suggestions)
        self.job_repo.update_status(job_id, "applying")


    def generate_suggestions(profiling_result: dict) -> list[dict]:
        client = MCPClient()

        result = client.call(
            tool="suggestions",
            payload={
                "profiling": profiling_result
            }
        )

        return result["suggestions"]


    
