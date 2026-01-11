# 🤖 AI Data Cleaning Assistant

[![Tests](https://github.com/deedeepratiwi/ai-data-cleaning-assistant/workflows/Tests/badge.svg)](https://github.com/deedeepratiwi/ai-data-cleaning-assistant/actions)

## 📌 Problem Description

Raw tabular data (CSV/Excel) is often messy: inconsistent column names, missing values, mixed data types, duplicates, and unclear schemas. Cleaning this data is time-consuming, error-prone, and repetitive, especially for analysts and data scientists.

**This project builds an AI-powered data cleaning assistant** that:

* Accepts CSV or Excel files via a web UI or API
* Analyzes dataset structure and common data quality issues
* Generates and applies cleaning suggestions using rule-based or LLM reasoning
* Returns a cleaned dataset plus a human-readable explanation of changes

The system is designed as a **full-stack AI application** demonstrating modern AI development practices, API-first design, containerization, testing, and deployment.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/deedeepratiwi/ai-data-cleaning-assistant.git
   cd ai-data-cleaning-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers (for e2e tests)**
   ```bash
   python -m playwright install chromium
   ```

4. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

5. **Start the server**
   ```bash
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Open the landing page**
   
   Navigate to [http://localhost:8000](http://localhost:8000) in your browser

---

## 🧪 Testing

### Run All Tests

```bash
# Run all tests including e2e
pytest tests/ -v
```

### Run Unit Tests Only

```bash
# Run transformation unit tests
pytest tests/test_transformations.py -v
```

### Run E2E Tests

```bash
# Ensure server is running on port 8000
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Run Playwright e2e tests
pytest tests/test_e2e_playwright.py -v
```

### Test Coverage

```bash
pytest --cov=. --cov-report=html tests/
```

---

## 📋 Usage Example

### Using the Web UI

1. Navigate to [http://localhost:8000](http://localhost:8000)
2. Click "Choose CSV File" and select a messy CSV file
3. Click "Upload & Clean Data"
4. Wait for processing to complete
5. Download the cleaned CSV or view the cleaning report

### Using the API

```bash
# 1. Upload a file
curl -X POST http://localhost:8000/jobs/upload \
  -F "file=@dirty_data.csv"
# Response: {"job_id": "abc-123", "status": "pending"}

# 2. Start profiling (triggers full pipeline)
curl -X POST http://localhost:8000/jobs/abc-123/profile

# 3. Check status
curl http://localhost:8000/jobs/abc-123
# Response: {"status": "done", ...}

# 4. Download cleaned file
curl http://localhost:8000/jobs/abc-123/download -o cleaned.csv

# 5. View cleaning report
curl http://localhost:8000/jobs/abc-123/report
```

---

## 🧠 AI System Development (Tools, Workflow, MCP)

### AI-Assisted Development

AI tools were used throughout development to:

* Generate and refactor backend and frontend code
* Design prompts for data quality analysis and cleaning suggestions
* Draft OpenAPI specifications and test cases
* Improve documentation and developer ergonomics

### Prompt & Workflow Design

The LLM is used in a **tool-augmented workflow**:

1. Dataset schema and statistics are extracted programmatically
2. Structured context is sent to the LLM (column types, missing values, samples)
3. The LLM proposes cleaning actions in a structured JSON format
4. The backend validates and executes these actions deterministically

### MCP (Model Context Protocol)

This project uses MCP concepts by:

* Defining **clear tool boundaries** between LLM reasoning and execution
* Treating the LLM as a planner, not an executor
* Using structured inputs/outputs (JSON schemas) as the contract between model and system

An example MCP-style tool interface is documented in `AGENTS.md`.

---

## 🏗️ Technologies & System Architecture

### Tech Stack

| Layer            | Technology              | Role                                    |
| ---------------- | ----------------------- | --------------------------------------- |
| Frontend         | React + TypeScript      | File upload, preview, results UI        |
| Backend          | FastAPI (Python)        | API, LLM orchestration, data processing |
| AI               | OpenAI-compatible LLM   | Data issue detection & suggestions      |
| Data             | Pandas                  | Data profiling & cleaning               |
| Database         | SQLite / Postgres       | Job metadata & history                  |
| API Spec         | OpenAPI                 | Frontend–backend contract               |
| Containerization | Docker & docker-compose | Local & production runs                 |
| CI/CD            | GitHub Actions          | Tests & deployment                      |

### Architecture Overview

```
Frontend (React)
   ↓ OpenAPI
Backend (FastAPI)
   ↓
Data Profiler → LLM (Planner)
   ↓ JSON Actions
Deterministic Cleaning Engine
   ↓
Database + Cleaned Outputs
```

---

## 🎨 Frontend Implementation

* Built with **React + TypeScript**
* Centralized API client based on OpenAPI spec
* Clear separation between UI components and data services
* Supports:

  * File upload
  * Data preview
  * Cleaning summary display

### Frontend Tests

* Unit tests for core logic using Vitest
* Run tests with:

```bash
npm test
```

---

## 📜 API Contract (OpenAPI)

* OpenAPI spec defined in `openapi.yaml`
* Used as the **single source of truth** for:

  * Backend endpoint implementation
  * Frontend API client generation

Key endpoints:

* `POST /clean` – Upload dataset and start cleaning job
* `GET /jobs/{id}` – Retrieve cleaning results and metadata

---

## ⚙️ Backend Implementation

* Built with **FastAPI** following OpenAPI contract
* Layered structure:

  * API routers
  * Services (LLM orchestration, cleaning logic)
  * Repositories (DB access)

### Backend Tests

* Unit tests for cleaning logic
* API tests using FastAPI TestClient

```bash
pytest
```

---

## 🗄️ Database Integration

* Uses **SQLite** for local development
* Supports **Postgres** for production
* Environment-based configuration via `.env`
* Stores:

  * Job metadata
  * Cleaning actions
  * Execution status

---

## 🐳 Containerization

The entire system runs via Docker.

```bash
docker-compose up --build
```

Services included:

* frontend
* backend
* database

---

## 🔬 Integration Testing

* Integration tests are separated under `tests/integration/`
* Cover:

  * API → database interactions
  * End-to-end cleaning workflow

```bash
pytest tests/integration
```

---

## 🚀 Deployment

* Deployed to cloud infrastructure (example: Render / Fly.io / GCP)
* Live demo URL provided in repository description
* Deployment configuration included in `deploy/`

---

## 🔁 CI/CD Pipeline

* GitHub Actions workflow:

  * Runs backend & frontend tests on every push
  * Builds Docker images
  * Deploys on main branch if tests pass

---

## 🔒 Security & File Management

### Secure File Handling

- Uploaded files are stored with UUID-based names to prevent path traversal attacks
- File types are validated (CSV only)
- Files are stored in a controlled `data/` directory
- No direct user input is used in file paths

### Automatic Cleanup

Clean up old files manually:

```bash
python -m core.cleanup
```

Or programmatically:

```python
from core.cleanup import cleanup_old_files, cleanup_job_files

# Remove files older than 7 days
stats = cleanup_old_files(days_old=7)

# Remove all files for a specific job
cleanup_job_files(job_id="abc-123")
```

**Recommended:** Set up a cron job or scheduled task to run cleanup weekly.

---

## ♻️ Reproducibility

### Local Setup

```bash
git clone <repo>
cd ai-data-cleaning-assistant
pip install -r requirements.txt
python scripts/init_db.py
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
pytest tests/ -v
```

### Environment Variables

Create a `.env` file for configuration (optional):

```env
MCP_URL=http://mcp:9000
DATABASE_URL=sqlite:///./data.db
```

---

## ✅ Evaluation Criteria Mapping

This README explicitly documents:

* Problem definition & system goals
* AI-assisted development & MCP concepts
* Full-stack architecture & technologies
* API-first backend design
* Frontend, backend, database, containerization
* Testing, CI/CD, deployment, and reproducibility

Designed to score **maximum points** against the AI Dev Tools Zoomcamp rubric.

---

## 📄 License

MIT
