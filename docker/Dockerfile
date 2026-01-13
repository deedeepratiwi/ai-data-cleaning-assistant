FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

COPY . /app/

ENV PORT=8000
EXPOSE $PORT

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
