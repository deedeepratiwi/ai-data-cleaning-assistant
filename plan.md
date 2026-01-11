# AI Data Cleaning

## Problem Description
Analysts and freelancers waste significant time cleaning messy CSV datasets before analysis. Existing tools are manual, non-reproducible, or opaque. This project builds an AI-assisted data cleaning system that analyzes uploaded datasets, proposes structured cleaning steps, executes them safely, and produces cleaned data along with reusable code and a transparent cleaning report.


## AI system development (tools, workflow, MCP)
You can explicitly document:
- AI coding assistants used during development
- Prompt design for analysis vs execution
- MCP tools for:
- Schema inspection
- Issue detection
- Cleaning step proposal
- Step execution

## Technologies & system architecture
- Frontend: React / Next.js (file upload, status, results)
- Backend: FastAPI (API + AI orchestration)
- AI: OpenAI / Claude via MCP-style tool calls
- DB: SQLite (local) → Postgres (prod)
- Automation: n8n (workflow orchestration or async jobs)
- Infra: Docker + docker-compose
- CI/CD: GitHub Actions

## Frontend implementation
A simple but well-structured frontend is enough:
- File upload
- Progress state
- Results page (download CSV, view report)

Key thing:
- Centralized API client
- Clear separation of concerns
- Add basic frontend tests (even a few):
- Upload validation
- API client mock

## API contract (OpenAPI)
Endpoints like:
- POST /datasets/upload
- POST /datasets/{id}/clean
- GET /datasets/{id}/result
- GET /datasets/{id}/report

## Backend implementation
Backend responsibilities are clear:
- Validate uploads
- Persist metadata
- Orchestrate AI calls
- Execute deterministic cleaning code
- Generate artifacts

You can:
- Structure services cleanly
- Write unit tests for:
    - Cleaning logic
    - Validation
- Follow OpenAPI strictly

## Database integration
Store:
- Dataset metadata
- Cleaning steps
- Status
- Output file paths

Support:
- SQLite for local dev
- Postgres for prod

## Containerization
- Dockerfile for frontend
- Dockerfile for backend
- docker-compose:
    - frontend
    - backend
    - db

## Integration testing
Integration test flows:
- Upload CSV
- Trigger cleaning
- Assert:
    - DB record created
    - Cleaned CSV exists
    - Report generated

## Deployment
Easy deployment options:
- Backend on Render / Fly.io
- Frontend on Vercel
- Or both containerized on one platform

You just need:
- A working URL
- Or screenshots + logs

## CI/CD
GitHub Actions pipeline:
- Run backend tests
- Run frontend tests
- Build Docker images
- Deploy on main branch

## Reproducibility
This project is:
- Deterministic
- Scriptable
- Easy to document

Clear README:
- Setup
- Run
- Test
- Deploy
---

## north star:

“Save analysts 1–3 hours per dataset, safely.”

## Problem statement (README-ready)

## Problem
Messy CSV datasets slow down analysis and introduce errors. Analysts often repeat the same manual cleaning steps without documentation, reproducibility, or reusable code.

## Solution
An AI-assisted data cleaning system that:
- Analyzes uploaded CSV datasets
- Detects common data quality issues
- Proposes structured cleaning steps
- Executes them safely
- Produces:
    - Cleaned dataset
    - Reusable cleaning code
    - Human-readable cleaning report

Non-goals (important for scope control)
- No automatic feature engineering
- No ML modeling
- No “perfect cleaning” guarantee

## Target user (so you don’t overbuild)
Primary user (start here)
- Freelancers
- Junior–mid data analysts
- Consultants
- Students working with CSVs

They want:
- Speed
- Explainability
- Reusable code
- Not fancy dashboards

## Core value proposition (what people pay for)
You are selling three outputs, not “AI”:
- Cleaned CSV
- Reusable cleaning script (Python / Pandas)
- Cleaning report (what changed + why)

## MVP feature set (VERY important)
✅ Included in v1 (Zoomcamp + public-ready)
Upload & validation
- CSV upload
- File size limit
- Row/column limits
- Schema preview

AI-assisted analysis
- Missing values
- Duplicates
- Type inconsistencies
- Invalid categories
- Simple outliers (IQR / z-score)

Cleaning execution
- Drop / fill nulls
- Type casting
- Deduplication
- Column renaming
- Category normalization

Outputs
- Cleaned CSV
- Cleaning script
- Cleaning report (Markdown / HTML)

Explicitly excluded (for now)
- Multi-file joins
- Time-series specific logic
- Custom user prompts
- Streaming data
- Auto-EDA charts

## System architecture
**High-level architecture**
```
Frontend (React)
   |
   | REST API (OpenAPI)
   |
Backend (FastAPI)
   ├─ Data validation
   ├─ MCP-based AI orchestration
   ├─ Deterministic cleaning engine
   ├─ Report generator
   |
Database (SQLite → Postgres)
   |
File storage (local / S3)
```

```
n8n → async orchestration / delivery
```

This architecture:
- Hits frontend + backend + API spec
- Is containerizable
- Is deployable
- Scales later

## MCP design (this is your differentiator)

You will explicitly implement MCP-style tools, not just mention them.
**MCP tools (v1)**
inspect_dataset(schema, sample_rows)
detect_issues(dataset_profile)
propose_cleaning_steps(issues)
apply_cleaning_step(step_id)
generate_report(changes)

Why this matters
- LLM does reasoning
- Code does execution
- You control compute + safety

## Frontend scope (don’t overdo it)
Pages
- Upload page
- Processing state
- Results page

UI goals
- Clean
- Minimal
- Explainable

No auth needed for v1

## Backend scope (clean & testable)
Core services
- DatasetService
- CleaningService
- AIOrchestrator (MCP)
- ReportService

Backend guarantees
- Never execute raw LLM code
- Only allow whitelisted operations
- Time-bounded processing

This makes it safe to sell.

## Database (just enough)

Tables:
- datasets
- cleaning_steps
- executions

SQLite locally, Postgres in prod.

## Testing strategy (realistic, not fake)
Unit tests
- Cleaning operations
- Validation logic
- Report generation

Integration tests
- Upload → clean → download
- DB + file system interaction

## Monetization path (after submission)

You are future-proofing from day one.

Phase 1 (after Zoomcamp)
- Pay-per-file
- Manual payment link
- Limited usage

Phase 2
- Usage credits
- Auth
- Higher limits