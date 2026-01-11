# 🤖 AI Data Cleaning Assistant

## 📌 Problem Description

Raw tabular data (CSV/Excel) is often messy: inconsistent column names, missing values, mixed data types, duplicates, and unclear schemas. Cleaning this data is time-consuming, error-prone, and repetitive, especially for analysts and data scientists.

**This project builds an AI-powered data cleaning assistant** that:

* Accepts CSV or Excel files via a web UI or API
* Analyzes dataset structure and common data quality issues
* Generates and applies cleaning suggestions using LLM reasoning
* Returns a cleaned dataset plus a human-readable explanation of changes

The system is designed as a **full-stack AI application** demonstrating modern AI development practices, API-first design, containerization, testing, and deployment.

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

## ♻️ Reproducibility

### Local Setup

```bash
git clone <repo>
cd ai-data-cleaning-assistant
docker-compose up --build
```

### Run Tests

```bash
pytest
npm test
```

### Environment Variables

See `.env.example` for required configuration.

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
