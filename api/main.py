from fastapi import FastAPI
from api.routes import jobs, upload, orchestrate, apply, download

app = FastAPI(
    title="AI Data Cleaning Assistant",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

from api.routes import report
app.include_router(jobs.router)
app.include_router(upload.router)
app.include_router(orchestrate.router)
app.include_router(apply.router)
app.include_router(download.router)
app.include_router(report.router)