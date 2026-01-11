"""
Cleanup utilities for removing temporary files
"""
import os
from pathlib import Path
from datetime import datetime, timedelta
from core.constants import DATA_DIR


def cleanup_old_files(days_old: int = 7) -> dict:
    """
    Remove uploaded and cleaned files older than specified days
    
    Args:
        days_old: Number of days after which files should be deleted
        
    Returns:
        dict: Statistics about cleaned up files
    """
    cutoff_time = datetime.now() - timedelta(days=days_old)
    stats = {
        "uploaded_deleted": 0,
        "cleaned_deleted": 0,
        "reports_deleted": 0
    }
    
    data_path = Path(DATA_DIR)
    
    # Clean uploaded files
    for csv_file in data_path.glob("*.csv"):
        if csv_file.stat().st_mtime < cutoff_time.timestamp():
            csv_file.unlink()
            stats["uploaded_deleted"] += 1
    
    # Clean cleaned files
    cleaned_dir = data_path / "cleaned"
    if cleaned_dir.exists():
        for csv_file in cleaned_dir.glob("*.csv"):
            if csv_file.stat().st_mtime < cutoff_time.timestamp():
                csv_file.unlink()
                stats["cleaned_deleted"] += 1
    
    # Clean reports
    reports_dir = data_path / "reports"
    if reports_dir.exists():
        for report_file in reports_dir.glob("*.md"):
            if report_file.stat().st_mtime < cutoff_time.timestamp():
                report_file.unlink()
                stats["reports_deleted"] += 1
    
    return stats


def cleanup_job_files(job_id: str) -> bool:
    """
    Remove all files associated with a specific job
    
    Args:
        job_id: The job ID to clean up
        
    Returns:
        bool: True if files were found and deleted
    """
    data_path = Path(DATA_DIR)
    deleted = False
    
    # Remove uploaded file
    uploaded_file = data_path / f"{job_id}.csv"
    if uploaded_file.exists():
        uploaded_file.unlink()
        deleted = True
    
    # Remove cleaned file
    cleaned_file = data_path / "cleaned" / f"{job_id}.csv"
    if cleaned_file.exists():
        cleaned_file.unlink()
        deleted = True
    
    # Remove report
    report_file = data_path / "reports" / f"{job_id}.md"
    if report_file.exists():
        report_file.unlink()
        deleted = True
    
    return deleted


if __name__ == "__main__":
    # Can be run as a script for manual cleanup
    stats = cleanup_old_files(days_old=7)
    print(f"Cleanup complete: {stats}")
