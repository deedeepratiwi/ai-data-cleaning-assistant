FROM python:3.11-slim

WORKDIR /app

COPY mcp /app/mcp
COPY transformations /app/transformations

RUN pip install fastapi uvicorn pandas

ENV PORT=9000
EXPOSE $PORT

CMD uvicorn mcp.app:app --host 0.0.0.0 --port $PORT
