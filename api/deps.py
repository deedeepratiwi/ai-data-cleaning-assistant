from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use /tmp for Cloud Run compatibility (filesystem is read-only except /tmp)
# Note: sqlite:////tmp/data.db uses 4 slashes (sqlite:/// + /tmp/data.db absolute path)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/data.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
