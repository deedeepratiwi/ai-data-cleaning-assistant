from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import jobs, upload, orchestrate, apply, download, report, suggestions

app = FastAPI(
    title="AI Data Cleaning Assistant",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Include API routers
app.include_router(jobs.router)
app.include_router(upload.router)
app.include_router(orchestrate.router)
app.include_router(apply.router)
app.include_router(download.router)
app.include_router(report.router)
app.include_router(suggestions.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve landing page at root
@app.get("/")
def read_root():
    return FileResponse("static/index.html")