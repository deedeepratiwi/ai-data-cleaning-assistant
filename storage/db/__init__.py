from .models import Base
from sqlalchemy import create_engine
import os

# Use /tmp for Cloud Run compatibility (filesystem is read-only except /tmp)
engine = create_engine(
    os.getenv("DATABASE_URL", "sqlite:////tmp/data.db"),
    connect_args={"check_same_thread": False}
)
