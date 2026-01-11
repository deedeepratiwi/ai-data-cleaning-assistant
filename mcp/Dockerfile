FROM python:3.11-slim

WORKDIR /app

COPY mcp /app/mcp
COPY transformations /app/transformations

RUN pip install fastapi uvicorn pandas

CMD ["uvicorn", "mcp.app:app", "--host", "0.0.0.0", "--port", "9000"]
