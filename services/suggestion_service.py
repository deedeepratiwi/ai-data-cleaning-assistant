from sqlalchemy.orm import Session
import pandas as pd
from pathlib import Path

from storage.db.repository import (
    JobRepository,
    ProfilingRepository,
    SuggestionRepository,
)
from agents.data_cleaning_agent import DataCleaningAgent
from services.job_service import can_transition
from core.constants import DATA_DIR

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
                suggestions = self._generate_simple_suggestions(job_id, profiling)
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
            # Note: This creates an in-process orchestration flow.
            # In production, consider using a message queue (Celery, RabbitMQ)
            # or workflow engine (n8n, Temporal) to avoid circular imports
            from services.apply_service import ApplyService
            apply_service = ApplyService(self.db)
            apply_service.run(job_id)

        except Exception:
            self.job_repo.update_status(job_id, "failed")
            raise

    def _generate_simple_suggestions(self, job_id: str, profiling) -> list[dict]:
        """Generate basic cleaning suggestions based on profiling data and actual data analysis"""
        suggestions = []
        
        # Load the actual data for more detailed analysis
        file_path = Path(DATA_DIR) / f"{job_id}.csv"
        df = pd.read_csv(file_path)
        
        # Common non-value indicators to check for
        non_value_indicators = [
            'UNKNOWN', 'unknown', 'Unknown',
            'ERROR', 'error', 'Error',
            'N/A', 'n/a', 'NA', 'na',
            'NULL', 'null', 'Null',
            'NONE', 'none', 'None',
        ]
        
        # Track which columns need which transformations
        columns_needing_non_value_replacement = set()
        columns_needing_standardization = set()
        columns_needing_auto_cast = set()
        
        # Analyze each column
        for col in df.columns:
            col_type = profiling.column_types.get(col, "object")
            
            # Check for non-value indicators in string columns
            if col_type == "object":
                # Get unique non-null values
                unique_values = df[col].dropna().astype(str).unique()
                
                # Check if any non-value indicators exist
                has_non_values = any(
                    any(nv in str(val) for nv in non_value_indicators)
                    for val in unique_values
                )
                
                if has_non_values:
                    columns_needing_non_value_replacement.add(col)
                
                # Check if column needs standardization (mixed casing or inconsistent formatting)
                # Skip columns that look like IDs or codes (contain mostly numbers/underscores)
                # We'll standardize if there are multiple unique values with letters
                col_lower = col.lower()
                is_likely_id = 'id' in col_lower or 'code' in col_lower or 'key' in col_lower
                
                if len(unique_values) > 1 and not is_likely_id:
                    # Check if values contain letters (not just numbers/symbols)
                    has_letters = any(any(c.isalpha() for c in str(v)) for v in unique_values)
                    if has_letters:
                        # Convert to lowercase for comparison
                        lower_values = [str(v).lower() for v in unique_values]
                        # Check for mixed casing or if standardization would help
                        if len(lower_values) != len(set(lower_values)) or any(
                            str(v) != str(v).title() for v in unique_values
                        ):
                            columns_needing_standardization.add(col)
                
                # Check if column is numeric stored as string
                try:
                    # Try to convert to numeric
                    numeric_test = pd.to_numeric(df[col], errors='coerce')
                    # If most non-null values convert successfully, it's likely numeric
                    non_null_count = df[col].notna().sum()
                    if non_null_count > 0:
                        converted_count = numeric_test.notna().sum()
                        if converted_count / non_null_count > 0.5:  # More than 50% are numeric
                            columns_needing_auto_cast.add(col)
                except (ValueError, TypeError):
                    pass
        
        # Generate suggestions in the right order:
        # 1. Replace non-values first (converts ERROR/UNKNOWN to NaN)
        for col in columns_needing_non_value_replacement:
            suggestions.append({
                "operation": "replace_non_values",
                "params": {"column": col}
            })
        
        # 2. Then standardize case for remaining string values
        for col in columns_needing_standardization:
            suggestions.append({
                "operation": "standardize_case",
                "params": {"column": col}
            })
        
        # 3. Then auto-cast numeric strings
        for col in columns_needing_auto_cast:
            suggestions.append({
                "operation": "auto_cast_type",
                "params": {"column": col}
            })
        
        # 4. Finally handle nulls (including those created by replace_non_values)
        for col, null_count in profiling.null_counts.items():
            col_type = profiling.column_types.get(col, "object")
            
            # Also check if we added nulls via non-value replacement
            additional_nulls = col in columns_needing_non_value_replacement
            
            if null_count > 0 or additional_nulls:
                # Skip if already suggested auto_cast (it will handle nulls)
                if col in columns_needing_auto_cast:
                    continue
                
                # Skip suggesting drop_null_rows for columns where we replaced non-values
                # Users likely want to keep these rows with NaN values
                if additional_nulls:
                    continue
                    
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


    
