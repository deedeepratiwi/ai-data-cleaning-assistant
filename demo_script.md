🎬 AI Data Cleaning Assistant — Demo Script

⏱️ Total time: ~6 minutes

Audience: technical reviewers, hiring managers, early users

0️⃣ Intro (30 seconds)

“This project is an AI-powered data cleaning assistant.
Users upload a raw CSV file, and the system automatically profiles the data, generates cleaning suggestions using an LLM, applies transformations, and returns a cleaned dataset — all fully automated and orchestrated.”

(Optional add:)

“The system is built with FastAPI, MCP for AI intelligence, and n8n for orchestration.”

1️⃣ Show Architecture (45 seconds)

Open docs/architecture.md or say verbally:

“The architecture is split into three layers:
- Main API: owns jobs, files, and state
- MCP server: handles LLM-based reasoning
- n8n: orchestrates the pipeline steps

This separation makes the system safe, scalable, and replaceable.”

Key line (important for reviewers):

“n8n contains no business logic — it only coordinates API calls.”

Start the System (30 seconds)

Terminal:

docker compose up --build


Say:

“Everything runs locally via Docker Compose — API, MCP server, and n8n.”

Open:

API: http://localhost:8000/docs

n8n: http://localhost:5678

3️⃣ Upload a CSV File (1 minute)

Use Swagger UI or curl.

Example CSV (mention verbally)

“This CSV contains missing values, inconsistent types, and unnecessary columns.”

Swagger:

POST /jobs/upload


Upload a file like raw_customers.csv.

Response:

{
  "job": {
    "id": "42438666-d8f5-4952-b514-c292ad66d8c0",
    "status": "pending"
  }
}


Say:

“Uploading a file creates a job and stores the raw data.”

4️⃣ Trigger the AI Pipeline (45 seconds)
POST /jobs/{job_id}/run


Say:

“This triggers an n8n workflow via a webhook.
From here, everything is asynchronous and automated.”


5️⃣ Show n8n Workflow Running (1 minute)

Open n8n UI → Workflow executions.

Explain each step:
- Profiling
- AI suggestions (via MCP)
- Apply transformations

Key line:

“Each step is retryable and idempotent. Failures don’t corrupt job state.”

6️⃣ Job Completion (30 seconds)

Check job status:

GET /jobs/{job_id}


Response:

{
  "status": "done"
}


Say:

“Once the job reaches done, the cleaned dataset is available.”


7️⃣ Download Cleaned Data (45 seconds)
GET /jobs/{job_id}/download


Browser downloads:

42438666_cleaned.csv


Open it briefly and show:
- Fewer nulls
- Cleaned columns
- Consistent types

Say:

“This is the final cleaned dataset, ready for analysis or ML.”

8️⃣ Why This Matters (45 seconds)

Close with:

“This project demonstrates:
- Real AI integration using MCP
- Production-grade orchestration with n8n
- Clean system boundaries
- End-to-end automation

It’s not a notebook demo — it’s a real, deployable system.”

Optional:

“This can be sold as a self-hosted workflow, API service, or internal data tool.”

Demo Checklist (Before Recording)
- Docker builds clean
- Sample CSV ready
- n8n workflow imported
- Swagger UI loads
- Download endpoint works