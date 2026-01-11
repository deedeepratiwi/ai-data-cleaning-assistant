import sys
import os

# Ensure project root is in sys.path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from storage.db.models import JobModel, ProfilingResult, SuggestionModel
from storage.db import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()