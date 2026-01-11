Your plan is strong and well-structured, but to actually deliver a working MVP with a landing page for file upload and download, you need to ensure the following are implemented and connected:

1. Frontend (Landing Page)

A React (or Next.js) page with:
File upload form (accepts CSV)
Progress/processing state
Download link for cleaned CSV
Link or display for cleaning report

2. API Endpoints (FastAPI)

POST /datasets/upload: Accepts file upload, returns dataset ID
POST /datasets/{id}/clean: Triggers cleaning, returns status
GET /datasets/{id}/result: Returns cleaned CSV for download
GET /datasets/{id}/report: Returns cleaning report (Markdown/HTML)

3. Backend Services

File validation and storage
DatasetService: Handles metadata, file paths
CleaningService: Runs deterministic cleaning steps
AIOrchestrator: Calls MCP tools (inspect, detect, propose, apply, report)
ReportService: Generates human-readable report

4. MCP Tools Implementation

Each MCP tool (inspect_dataset, detect_issues, etc.) must be implemented as callable Python functions/classes, not just prompts.

5. Database

Tables: datasets, cleaning_steps, executions (ensure models and migrations exist)

6. Testing

At least one integration test: upload → clean → download

7. Dockerization

Dockerfile for backend and frontend
docker-compose.yaml to run both + db

8. Frontend-Backend Connection

API client in frontend to call backend endpoints
Handle file upload, poll for status, show download/report links