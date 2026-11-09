FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv pip install --system -e ".[dev]"
COPY apps/worker /app
CMD ["python", "-m", "worker.main"]
