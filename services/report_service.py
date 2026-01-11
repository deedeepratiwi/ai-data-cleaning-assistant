import os
from pathlib import Path
from storage.db.repository import JobRepository, SuggestionRepository
from core.constants import DATA_DIR

class ReportService:
    def __init__(self, db):
        self.db = db
        self.job_repo = JobRepository(db)
        self.suggestion_repo = SuggestionRepository(db)

    def generate_report(self, job_id: str) -> str:
        job = self.job_repo.get(job_id)
        suggestions = self.suggestion_repo.get_by_job_id(job_id)
        if not job or not suggestions:
            return "No report available."
        report = f"# Cleaning Report for Job {job_id}\n\n"
        report += f"**Original file:** {job.original_filename}\n\n"
        report += "## Cleaning Steps Applied\n"
        for i, step in enumerate(suggestions.suggestions, 1):
            op = step.get("operation", "unknown")
            params = step.get("params", {})
            report += f"{i}. **{op}**: {params}\n"
        report += "\n---\n"
        report += "This report was generated automatically."
        return report

    def save_report(self, job_id: str, report: str):
        report_dir = Path(DATA_DIR) / "reports"
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"{job_id}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        return str(report_path)
