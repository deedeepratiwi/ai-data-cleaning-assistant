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
        self.agent = None if llm_client is None else DataCleaningAgent(llm_client)

    def run(self, job_id: str):
        try:
            job = self.job_repo.get(job_id)
            if not job:
                raise ValueError("Job not found")

            # Allow running if job is in 'suggesting' status (already set by profiling)
            # or if it can transition to suggesting
            if job.status != "suggesting" and not can_transition(job.status, "suggesting"):
                raise ValueError("Invalid job state")

            profiling = self.profile_repo.get_by_job_id(job_id)
            if not profiling:
                raise ValueError("Profiling missing")

            # Generate simple rule-based suggestions if no LLM
            if self.agent is None:
                suggestions = self._generate_simple_suggestions(profiling)
            else:
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
            
            # Auto-trigger applying phase
            from services.apply_service import ApplyService
            apply_service = ApplyService(self.db)
            apply_service.run(job_id)

        except Exception:
            self.job_repo.update_status(job_id, "failed")
            raise

    def _generate_simple_suggestions(self, profiling) -> list[dict]:
        """Generate basic cleaning suggestions based on profiling data"""
        suggestions = []
        
        # For each column with nulls, suggest filling with 0 for numbers or dropping rows
        for col, null_count in profiling.null_counts.items():
            if null_count > 0:
                col_type = profiling.column_types.get(col, "object")
                if "int" in col_type or "float" in col_type:
                    suggestions.append({
                        "operation": "fill_nulls",
                        "params": {"column": col, "value": 0}
                    })
                else:
                    suggestions.append({
                        "operation": "drop_null_rows",
                        "params": {"column": col}
                    })
        
        return suggestions


    def generate_suggestions(profiling_result: dict) -> list[dict]:
        client = MCPClient()

        result = client.call(
            tool="suggestions",
            payload={
                "profiling": profiling_result
            }
        )

        return result["suggestions"]


    
