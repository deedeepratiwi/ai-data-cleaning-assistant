JOB_STATUS_TRANSITIONS = {
    "pending": ["profiling"],
    "profiling": ["suggesting", "failed"],
    "suggesting": ["applying", "failed"],
    "applying": ["done", "failed"],
    "done": [],
    "failed": ["profiling"],  # 👈 retry allowed
}

# Use /tmp for Cloud Run compatibility (filesystem is read-only except /tmp)
DATA_DIR = "/tmp/data"
