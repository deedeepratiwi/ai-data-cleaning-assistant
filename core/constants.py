JOB_STATUS_TRANSITIONS = {
    "pending": ["profiling"],
    "profiling": ["suggesting", "failed"],
    "suggesting": ["applying", "failed"],
    "applying": ["done", "failed"],
    "done": [],
    "failed": ["profiling"],  # 👈 retry allowed
}

DATA_DIR = "data"
